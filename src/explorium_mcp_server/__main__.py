from . import tools_businesses
from . import tools_prospects

from ._shared import mcp


def main():
    print("Starting Explorium MCP server...")
    mcp.run()


if __name__ == "__main__":
    main()
