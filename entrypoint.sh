#!/bin/sh
exec npx mcp-remote https://mcp-docker-registry.explorium.ai/mcp \
  --header "Authorization: Bearer ${API_ACCESS_TOKEN}"
