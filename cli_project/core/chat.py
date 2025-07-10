from typing import Protocol, Union
from mcp_client import MCPClient
from core.tools import ToolManager
from anthropic.types import MessageParam


class AIService(Protocol):
    """Protocol for AI services that can be used with Chat."""
    async def generate(self, prompt: str) -> str:
        ...


class Chat:
    def __init__(self, ai_service: AIService, clients: dict[str, MCPClient]):
        self.ai_service: AIService = ai_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        await self._process_query(query)
        
        # For now, we'll use a simple approach without tool integration
        # Build the conversation context from messages
        conversation = ""
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            if isinstance(content, str):
                conversation += f"{role}: {content}\n"
            elif isinstance(content, list):
                # Handle list content (text blocks)
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                conversation += f"{role}: {' '.join(text_parts)}\n"
        
        # Get response from AI service
        final_text_response = await self.ai_service.generate(conversation)
        
        return final_text_response
