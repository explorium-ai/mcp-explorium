## Explorium Business Data Hub


<p>
  <a href="https://github.com/explorium-ai/mcp-explorium/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Node.js-v24+-green.svg" alt="Node.js Version">
  <img src="https://img.shields.io/badge/MCP-Compatible-blueviolet" alt="MCP Compatible">
  <img src="https://img.shields.io/badge/Claude-Ready-orange" alt="Claude Ready">
  <img src="https://img.shields.io/badge/OpenAI-Compatible-lightgrey" alt="OpenAI Compatible">
  <img src="https://img.shields.io/badge/TypeScript-Powered-blue" alt="TypeScript">
</p>

<img src="logo.png" alt="Explorium Logo" width="90">

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

### Examples

**Example 1: Partnership Opportunity Research**
```
Who should I contact for partnership with monday.com? Get anyone who can promote a partnership with them. Bring me all the contact details you can find
```

**Example 2: Business Challenge Analysis**
```
What are the business challenges of amazon?
```

**Example 3: Leadership Team Discovery**
```
Get the engineering leadership team at Palo Alto Networks
```

## Installation

<details>
<summary><b>Install in Claude Desktop</b></summary>

#### Remote Server Connection

Open Claude Desktop and navigate to Settings > Connectors > Add Custom Connector. Enter the name as `Explorium` and the remote MCP server URL as `https://mcp.explorium.ai/mcp`.

#### Local Server Connection

Open Claude Desktop developer settings and edit your `claude_desktop_config.json` file to add the following configuration. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

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

</details>

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

#### Cursor Remote Server Connection

```json
{
  "mcpServers": {
    "explorium": {
      "url": "https://mcp.explorium.ai/mcp"
    }
  }
}
```

#### Cursor Local Server Connection

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

</details>

<details>
<summary><b>Install in Windsurf</b></summary>

Add this to your Windsurf MCP config file. See [Windsurf MCP docs](https://docs.windsurf.com/windsurf/cascade/mcp) for more info.

#### Windsurf Remote Server Connection

```json
{
  "mcpServers": {
    "explorium": {
      "serverUrl": "https://mcp.explorium.ai/mcp"
    }
  }
}
```

#### Windsurf Local Server Connection

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

</details>

<details>
<summary><b>Install in VS Code</b></summary>

Add this to your VS Code MCP config file. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

#### VS Code Remote Server Connection

```json
"mcp": {
  "servers": {
    "explorium": {
      "type": "http",
      "url": "https://mcp.explorium.ai/mcp"
    }
  }
}
```

#### VS Code Local Server Connection

```json
"mcp": {
  "servers": {
    "explorium": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.explorium.ai/mcp"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Zed</b></summary>

It can be installed via [Zed Extensions](https://zed.dev/extensions?query=Explorium) or you can add this to your Zed `settings.json`. See [Zed Context Server docs](https://zed.dev/docs/assistant/context-servers) for more info.

```json
{
  "context_servers": {
    "Explorium": {
      "command": {
        "path": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.explorium.ai/mcp"]
      },
      "settings": {}
    }
  }
}
```

</details>

<details>
<summary><b>Install in Cline</b></summary>

You can easily install Explorium through the [Cline MCP Server Marketplace](https://cline.bot/mcp-marketplace) by following these instructions:

1. Open **Cline**.
2. Click the hamburger menu icon (☰) to enter the **MCP Servers** section.
3. Use the search bar within the **Marketplace** tab to find _Explorium_.
4. Click the **Install** button.

</details>



<details>
<summary><b>Install in Roo Code</b></summary>

Add this to your Roo Code MCP configuration file. See [Roo Code MCP docs](https://docs.roocode.com/features/mcp/using-mcp-in-roo) for more info.

#### Roo Code Remote Server Connection

```json
{
  "mcpServers": {
    "explorium": {
      "type": "streamable-http",
      "url": "https://mcp.explorium.ai/mcp"
    }
  }
}
```

#### Roo Code Local Server Connection

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

</details>

<details>
<summary><b>Install in Gemini CLI</b></summary>

See [Gemini CLI Configuration](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html) for details.

1. Open the Gemini CLI settings file. The location is `~/.gemini/settings.json` (where `~` is your home directory).
2. Add the following to the `mcpServers` object in your `settings.json` file:

```json
{
  "mcpServers": {
    "explorium": {
      "httpUrl": "https://mcp.explorium.ai/mcp"
    }
  }
}
```

Or, for a local server:

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

If the `mcpServers` object does not exist, create it.

</details>



<details>
<summary><b>Install in JetBrains AI Assistant</b></summary>

See [JetBrains AI Assistant Documentation](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html) for more details.

1. In JetBrains IDEs go to `Settings` -> `Tools` -> `AI Assistant` -> `Model Context Protocol (MCP)`
2. Click `+ Add`.
3. Click on `Command` in the top-left corner of the dialog and select the As JSON option from the list
4. Add this configuration and click `OK`

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

5. Click `Apply` to save changes.
6. The same way explorium could be added for JetBrains Junie in `Settings` -> `Tools` -> `Junie` -> `MCP Settings`

</details>

<details>
<summary><b>Install in Kiro</b></summary>

See [Kiro Model Context Protocol Documentation](https://kiro.dev/docs/mcp/configuration/) for details.

1. Navigate `Kiro` > `MCP Servers`
2. Add a new MCP server by clicking the `+ Add` button.
3. Paste the configuration given below:

```json
{
  "mcpServers": {
    "Explorium": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.explorium.ai/mcp"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

4. Click `Save` to apply the changes.

</details>



## Connecting to Explorium MCP

For advanced users or other MCP clients, you can connect using these methods:

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
</parameter>

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
