# Explorium API MCP Server

[![mcp-explorerium-ci](https://github.com/explorium-ai/mcp-explorium/actions/workflows/ci.yml/badge.svg)](https://github.com/explorium-ai/mcp-explorium/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/explorium-mcp-server.svg)](https://badge.fury.io/py/explorium-mcp-server)
[![Python Versions](https://img.shields.io/pypi/pyversions/explorium-mcp-server.svg)](https://pypi.org/project/explorium-mcp-server/)

The Explorium MCP Server is a [Model Context Protocol](https://modelcontextprotocol.io/introduction) server used to
interact with the [Explorium API](https://developers.explorium.ai/reference/overview). It enables AI assistants to
access Explorium's business and prospect data lookup capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Setup for Development](#setup-for-development)
- [Running Locally](#running-locally)
- [Usage with AI Assistants](#usage-with-ai-assistants)
    - [Claude Desktop](#usage-with-claude-desktop)
    - [Cursor](#usage-with-cursor)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Continuous Integration](#continuous-integration)
- [Building and Publishing](#building-and-publishing)
- [License](#license)

## Overview

The Explorium MCP Server allows AI assistants to access the extensive business and prospects databases from Explorium.
This enables AI tools to provide accurate, up-to-date information about companies, industries, and professionals
directly in chat interfaces.

## Installation

Install the Explorium MCP Server from PyPI:

```bash
pip install explorium-mcp-server
```

The package requires Python 3.10 or later.

## Setup for Development

1. Clone the repository:

```bash
git clone https://github.com/explorium-ai/mcp-explorium.git
cd mcp-explorium
```

2. Set up the development environment using `uv`:

```bash
# Install uv if you don't have it
pip install uv

# Create and activate the virtual environment with all development dependencies
uv sync --group dev
```

3. Create a `.env` file in the root directory with your Explorium API key:

```
EXPLORIUM_API_KEY=your_api_key_here
```

To obtain an API key, follow the instructions in
the [Explorium API documentation](https://developers.explorium.ai/reference/getting_your_api_key).

## Running Locally

```bash
mcp dev local_dev_server.py
```

## Usage with AI Assistants

### Usage with Claude Desktop

1. Follow the [official Model Context Protocol guide](https://modelcontextprotocol.io/quickstart/user) to install Claude
   Desktop and set it up to use MCP servers.

2. Add this entry to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "Explorium": {
      "command": "python",
      "args": [
        "-m",
        "explorium_mcp_server"
      ],
      "env": {
        "EXPLORIUM_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

For development, you can use this configuration instead:

```json
{
  "mcpServers": {
    "Explorium": {
      "command": "<UV_INSTALL_PATH>",
      "args": [
        "run",
        "--directory",
        "<REPOSITORY_PATH>",
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

Replace all placeholders with your actual paths and API key.

### Usage with Cursor

Cursor has [built-in support for MCP servers](https://docs.cursor.com/context/model-context-protocol).

To configure it to use the Explorium MCP server:

1. Go to `Cursor > Settings > Cursor Settings > MCP`
2. Add an "Explorium" entry with this command:

For development, use:

```bash
uv run --directory <repo_path> mcp run local_dev_server.py
```

You may turn on "Yolo mode" in Cursor settings to use tools without confirming under
`Cursor > Settings > Cursor Settings > Features > Chat > Enable Yolo mode`.

## Project Structure

```
mcp-explorium/
├── .github/workflows/        # CI/CD configuration
│   └── ci.yml               # Main CI workflow
├── src/                      # Source code
│   └── explorium_mcp_server/
│       ├── __init__.py      # Package initialization
│       ├── __main__.py      # Entry point for direct execution
│       ├── models/          # Data models and schemas
│       └── tools/           # MCP tools implementation
├── tests/                    # Test suite
├── .env                      # Local environment variables (not in repo)
├── local_dev_server.py       # Development server script
├── Makefile                  # Development shortcuts
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # Project documentation
```

## Development Workflow

1. Set up the environment as described in [Setup for Development](#setup-for-development)
2. Make your changes to the codebase
3. Format your code:

```bash
make format
```

4. Run linting checks:

```bash
make lint
```

5. Run tests:

```bash
make test
```

## Continuous Integration

The project uses GitHub Actions for CI/CD. The workflow defined in `.github/workflows/ci.yml` does the following:

1. **Version Check**: Ensures the version in `pyproject.toml` is incremented before merging to main
2. **Linting**: Runs code style and formatting checks using `ruff`
3. **Testing**: Runs the test suite with coverage reporting
4. **Deployment**: Tags the repo with the version from `pyproject.toml` when merged to main

## Building and Publishing

### Building the Package

To build the package for distribution:

1. Update the version in `pyproject.toml` (required for every new release)
2. Run the build command:

```bash
uv build
```

This creates a `dist/` directory with the built package.

### Publishing to PyPI

To publish the package to PyPI:

1. Ensure you have `twine` installed:

```bash
uv pip install twine
```

2. Upload the built package to PyPI:

```bash
twine upload dist/*
```

You'll need to provide your PyPI credentials or configure them in a `.pypirc` file.

### Automatic Versioning and Tagging

When changes are merged to the main branch, the CI workflow automatically:

1. Tags the repository with the version from `pyproject.toml`
2. Pushes the tag to GitHub
