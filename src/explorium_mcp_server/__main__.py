from .tools import businesses  ## noqa: F401
from .tools import prospects  ## noqa: F401
from .tools import session  ## noqa: F401

from .tools.shared import mcp, logger
from .storage.session import get_connection


def main():
    logger.info("Starting Explorium MCP Server")
    # Initialize the database connection
    get_connection()
    mcp.run()


if __name__ == "__main__":
    main()
