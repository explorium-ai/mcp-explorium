# Explorium API MCP Server
This MCP server is used to interact with the Explorium API.

## Setup

This project uses `uv` to manage dependencies and run the server.
To get started, install it and activate the virtual environment:

```bash
pip install uv

uv sync
```


## Tools

The MCP server provides tools for the Business and Prospect APIs described in the [Explorium API documentation](https://developers.explorium.ai/reference/getting-started-with-explorium-admin).

## Usage with Claude Desktop

Get the install path of the `uv`:

```bash
which uv
```

Follow the official guide to install Claude Desktop and set it up to use MCP servers:

https://modelcontextprotocol.io/quickstart/user

Then, add this entry to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "Explorium": {
      "command": "/Users/yotamfrid/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/Users/yotamfrid/work/explorium-ai/mcp-explorium",
        "--with",
        "mcp",
        "mcp",
        "run",
        "src/mcp_explorium/server.py"
      ],
      "env": {
        "EXPLORIUM_API_KEY": "<EXPLORIUM_API_KEY>"
      }
    }
  }
}
```

Be sure to replace all the `<PLACEHOLDERS>` with the actual values.
