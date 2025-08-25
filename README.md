# Explorium Business Data Hub

<img src="logo.png" alt="Explorium Logo" width="180">

**Discover companies, contacts, and business insights—powered by dozens of trusted external data sources.**

This repository contains the configuration and setup files for connecting to Explorium's Model Context Protocol (MCP) server, enabling AI tools to access comprehensive business intelligence data.

## Overview

The **Explorium Business Data Hub** provides AI tools with access to:

- **Company Search & Enrichment**: Find companies by name, domain, or attributes with detailed firmographics
- **Contact Discovery**: Locate and enrich professional contact information  
- **Business Intelligence**: Access technology stack, funding history, growth signals, and business events
- **Real-Time Data**: Up-to-date information from dozens of trusted external data sources
- **Workflow Integration**: Seamlessly integrate business data into AI-powered workflows

Search any company or professional for everything from emails and phone numbers to roles, growth signals, tech stack, business events, website changes, and more. Find qualified leads, research prospects, identify talent, or craft personalized outreach—all without leaving your AI tool.

## Connecting to Explorium MCP

You can connect your AI tool to Explorium using the Model Context Protocol (MCP) through several methods:

### Streamable HTTP (Recommended)

- **URL**: `https://mcp.explorium.ai/mcp`
- **JSON config**:
```json
{
  "mcpServers": {
    "Explorium": {
      "url": "https://mcp.explorium.ai/mcp"
    }
  }
}
```

### SSE (Server-Sent Events)

- **URL**: `https://mcp.explorium.ai/sse`
- **JSON config**:
```json
{
  "mcpServers": {
    "Explorium": {
      "url": "https://mcp.explorium.ai/sse"
    }
  }
}
```

### STDIO (Local Server)

- **JSON config**:
```json
{
  "mcpServers": {
    "explorium": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.explorium.ai/mcp"]
    }
  }
}
```

## API Key Requirements

**Important**: Different connection methods have different authentication requirements:

- ✅ **Claude Desktop Extension** - No API key required
- ✅ **MCP Remote Connections** (Streamable HTTP/SSE/STDIO) - No API key required  
- 🔑 **Docker Self-Hosting** - Requires API key

### Getting Your API Key

For Docker deployment, you'll need an API access token. Get yours at: [https://admin.explorium.ai/api-key](https://admin.explorium.ai/api-key)

## Docker Deployment

This repository includes Docker configuration for self-hosting:

```bash
# Build the Docker image
docker build -t explorium-mcp .

# Run the container with API access token
docker run -e API_ACCESS_TOKEN=your_explorium_access_token explorium-mcp
```

**Required Environment Variables:**
- `API_ACCESS_TOKEN` - Your Explorium API access token for authentication (get it [here](https://admin.explorium.ai/api-key))

You can also use a `.env` file or docker-compose for easier management:

```yaml
# docker-compose.yml
version: '3.8'
services:
  explorium-mcp:
    build: .
    ports:
      - "44280:44280"
    environment:
      - API_ACCESS_TOKEN=${API_ACCESS_TOKEN}
```

## Available Tools

Once connected, your AI tool will have access to tools for:

- **Business Matching**: Find companies by name, domain, or business ID
- **Business Enrichment**: Get detailed firmographics, technographics, and business intelligence
- **Business Events**: Track funding rounds, office changes, hiring trends, and company developments
- **Prospect Discovery**: Search for professionals and contacts within companies
- **Prospect Enrichment**: Access contact information, work history, and professional profiles
- **Prospect Events**: Track role changes, company moves, and career milestones


## Troubleshooting Connection Issues

If you're experiencing issues connecting your AI tool to Explorium MCP:

1. **Check MCP Client Support**  
   Verify that your AI tool supports MCP clients and can connect to MCP servers. Not all AI tools have this capability built-in yet.

2. **Verify Remote Server Support**  
   Some AI tools have MCP clients but don't support remote connections. If this is the case, you may still be able to connect using our Docker configuration or local server setup.

3. **Request MCP Support**  
   If your AI tool doesn't support MCP at all, we recommend reaching out to the tool's developers to request MCP server connection support.

## Configuration Files

This repository contains:

- `package.json` - Node.js dependencies and scripts
- `manifest.json` - Extension metadata and configuration
- `Dockerfile` - Container configuration for self-hosting
- `server/index.js` - Placeholder file (does not contain actual MCP implementation)
- `entrypoint.sh` - Docker container entry point

**Important Note**: The `server/index.js` file in this repository is just a placeholder and does not contain the actual MCP server implementation. To use Explorium MCP, you need to connect to the remote server at `https://mcp.explorium.ai/mcp` using `mcp-remote` or through the connection methods described above. The actual MCP server is hosted by Explorium and accessible via the remote URLs.

## Documentation & Support

- [API Documentation](https://developers.explorium.ai/reference/agentsource-mcp)
- [Support & Help Center](https://developers.explorium.ai/reference/support-help-center)
- [Explorium Homepage](https://www.explorium.ai/mcp/)

For technical support, contact [support@explorium.ai](mailto:support@explorium.ai).



## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---