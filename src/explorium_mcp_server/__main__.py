from . import tools_businesses
from . import tools_prospects

from ._shared import mcp, logger


def main():
    logger.info("Starting Explorium MCP Server")
    mcp.run()


if __name__ == "__main__":
    main()
