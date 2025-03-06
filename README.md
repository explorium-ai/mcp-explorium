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

## Running Locally

When developing locally, use `local_dev_server.py` to expose the MCP server to local clients.

You can test it with the MCP Inspector:

```bash
mcp dev local_dev_server.py
```

Create an `.env` file in the root of the repository with an
`EXPLORIUM_API_KEY` environment variable if it's not already configured.

### Usage with Claude Desktop

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
        "--with",
        "dotenv",
        "--with",
        "pydantic",
        "--with",
        "requests",
        "mcp",
        "run",
        "local_dev_server.py"
      ],
      "env": {
        "EXPLORIUM_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

Be sure to replace all the `<PLACEHOLDERS>` with the actual values.

Run `which uv` to get your `uv` install path.

### Usage with Cursor

Cursor has [built-in support for MCP servers](https://docs.cursor.com/context/model-context-protocol).

To configure it to use the Explorium MCP server, go to
`Cursor > Settings > Cursor Settings > MCP` and add an "Explorium" entry
with this command:

```bash
uv run --directory repo_path --with mcp --with dotenv --with pydantic --with requests mcp run local_dev_server.py
```

Make sure to replace `repo_path` with the actual path to the repository.

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

