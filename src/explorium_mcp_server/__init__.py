"""Explorium MCP server for interacting with the Explorium API."""

try:
    from importlib.metadata import version

    __version__ = version("explorium-mcp-server")
except ImportError:
    # Package is not installed
    __version__ = "unknown"
