# MCP Chat with Google Gemini

MCP Chat is a command-line interface application that enables interactive chat capabilities with Google's Gemini AI models through the Google GenAI API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Google Gemini API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
GEMINI_API_KEY=""  # Enter your Google Gemini API key
GEMINI_MODEL="gemini-1.5-flash"  # Specify the Gemini model to use
USE_UV=1  # Optional: Use UV for MCP server execution
```

### Step 2: Get your Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file

### Step 3: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install google-genai python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the Gemini model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## Troubleshooting

### Windows: Subprocess Cleanup Warnings

If you see `ResourceWarning` or `unclosed transport` warnings on Windows, you can suppress them by setting an environment variable before running:

**PowerShell:**
```powershell
$env:PYTHONWARNINGS="ignore::ResourceWarning"; uv run main.py
```

**Command Prompt:**
```cmd
set PYTHONWARNINGS=ignore::ResourceWarning && uv run main.py
```

These warnings don't affect functionality - they're just cleanup noise from Windows asyncio subprocess handling.

## Available Gemini Models

You can configure different Gemini models in your `.env` file:

- `gemini-1.5-flash`
- `gemini-1.5-pro` 
- `gemini-2.0-flash` 
- `gemini-2.5-pro`

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

### Customizing AI Service

The application uses a generic `AIService` protocol, making it easy to switch between different AI providers. The current implementation uses Google Gemini, but you can extend it to support other providers by implementing the `AIService` protocol.

### Linting and Typing Check

There are no lint or type checks implemented.
