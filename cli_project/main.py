import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
# Replace Anthropic/Claude with Google Gemini
from google import genai

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()

# Gemini Config
gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
gemini_api_key = os.getenv("GEMINI_API_KEY", "")

assert gemini_model, "Error: GEMINI_MODEL cannot be empty. Update .env"
assert gemini_api_key, "Error: GEMINI_API_KEY cannot be empty. Update .env"

# Initialize Gemini client
gemini_client = genai.Client(api_key=gemini_api_key)

class GeminiService:
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model

    async def generate(self, prompt: str) -> str:
        # Use the new Google GenAI SDK API
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=512
            )
        )
        return str(response.text)

async def main():
    gemini_service = GeminiService(
        client=gemini_client,
        model=gemini_model
    )

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = (
        ("uv", ["run", "mcp_server.py"])
        if os.getenv("USE_UV", "0") == "1"
        else ("python", ["mcp_server.py"])
    )

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(command="uv", args=["run", server_script])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            ai_service=gemini_service  # Pass Gemini service as ai_service
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
