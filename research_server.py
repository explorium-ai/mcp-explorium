from dotenv import load_dotenv

load_dotenv()

print("Starting local research MCP server...")
from src.explorium_mcp_server import mcp_server_research

mcp = mcp_server_research.research_mcp
# mcp.settings.port = 3000
# mcp.run(transport="sse")
