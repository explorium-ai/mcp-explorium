import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv

load_dotenv()

print("Starting local MCP server...")
from explorium_mcp_server import __main__  # noqa: F401
from explorium_mcp_server.tools.shared import mcp  # noqa: F401

print("MCP server started successfully.")
