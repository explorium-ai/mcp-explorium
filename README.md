# Explorium API MCP Server
This MCP server is used to interact with the Explorium API.

Note: this is the README for developing the MCP server. For usage instructions, see the [README-pypi.md](README-pypi.md).

## Setup

Clone the repository:

```bash
git clone https://github.com/explorium-ai/mcp-explorium.git
cd mcp-explorium
```

Install uv and activate the virtual environment:

```bash
pip install uv
uv sync --group dev
```

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
      "command": "<UV_INSTALL_PATH>",
      "args": [
        "run",
        "--directory",
        "<REPOSITORY_PATH>",
        "--with",
        "mcp",
        "mcp",
        "run",
        "src/explorium_mcp_server/__main__.py"
      ],
      "env": {
        "EXPLORIUM_API_KEY": "<EXPLORIUM_API_KEY>"
      }
    }
  }
}
```

Be sure to replace all the `<PLACEHOLDERS>` with the actual values.

## Building and Deploying

To build the MCP server, run:

```bash
uv build
```

This will create a `dist` directory with the built package.

You may then deploy the package to PyPI using the following command:

```bash
twine upload dist/*
```

