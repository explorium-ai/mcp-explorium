#!/bin/bash
set -e

# Check APP_TYPE environment variable to determine which app to run
if [ "$APP_TYPE" = "agent-ui" ]; then
    echo "Starting Agent UI..."
    cd /app/agent-ui
    serve -s dist -l 3000
elif [ "$APP_TYPE" = "mcp" ]; then
    echo "Starting MCP Server..."
    # Activate virtual environment
    source .venv/bin/activate
    cd /app
    langgraph dev --host 0.0.0.0
else
    echo "Error: APP_TYPE must be set to 'agent-ui' or 'mcp'"
    exit 1
fi

# Execute additional command if provided
exec "$@"