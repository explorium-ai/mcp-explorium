# Explorium API MCP Server
This MCP server is used to interact with the Explorium API.

## Setup

This project uses `uv` to manage dependencies and run the server.
To get started, install it and activate the virtual environment:

```bash
pip install uv

uv sync
```

Create a `.env` file in the root of the repository and add your Explorium API key:

```
EXPLORIUM_API_KEY=<YOUR_API_KEY>
```

## Tools

The MCP server provides tools for the Business and Prospect APIs described in the [Explorium API documentation](https://developers.explorium.ai/reference/getting-started-with-explorium-admin).

## Usage with Claude Desktop

Get the install path of the `uv` binary:

```bash
which uv
```

Follow the official guide to install Claude Desktop and set it up to use MCP servers:

https://modelcontextprotocol.io/quickstart/user

Then, add this entry to your `claude_desktop_config.json` file:

```json
  "mcpServers": {
    "Explorium": {
      "command": "<RESULT OF which uv>",
      "args": [
        "run",
        "--directory",
        "<ABSOLUTE PATH TO REPOSITORY>",
        "--with",
        "mcp",
        "mcp",
        "run",
        "src/mcp_explorium/server.py"
      ]
    }
  }
```

Replace `<RESULT OF which uv>` with the result of the `which uv` command above, and `<ABSOLUTE PATH TO REPOSITORY>` with the absolute path to the repository on your machine.