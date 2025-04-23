from .tools import businesses  ## noqa: F401
from .tools import prospects  ## noqa: F401

from .tools.shared import mcp, logger


def main():
    logger.info("Starting Explorium MCP Server")
    mcp.run()


if __name__ == "__main__":
    main()
