from dotenv import load_dotenv

load_dotenv()

print("Starting local MCP server...")
from src.explorium_mcp_server import __main__
from src.explorium_mcp_server._shared import mcp
