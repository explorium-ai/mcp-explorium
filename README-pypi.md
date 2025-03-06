## 🌎 Explorium MCP Server
Explorium MCP server is a [Model Context Protocol](https://modelcontextprotocol.io/introduction) server for interacting with the [Explorium API](https://developers.explorium.ai/reference/overview).

### Obtain an Explorium API key

Follow the instructions in the [Explorium API documentation](https://developers.explorium.ai/reference/getting_your_api_key) to obtain an API key.

Your API key will be used to authenticate your requests to the Explorium API through the MCP server.

### Usage with Claude Desktop

To use the MCP server with Claude Desktop, add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "Explorium": {
      "command": "python",
      "args": ["-m", "explorium_mcp_server"],
      "env": {
        "EXPLORIUM_API_KEY": "MY_API_KEY"
      }
    }
  }
}
```

Replace `MY_API_KEY` with your actual Explorium API key.

Replace `python` with the path to your Python executable (such as `python3`).