# Gemini CLI Extension - Vibe Prospecting

This repository contains a Gemini CLI extension for accessing Vibe Prospecting's B2B data platform via MCP Remote with OAuth authentication.

## Quick Install

```bash
gemini extensions install https://github.com/explorium-ai/mcp-explorium
```

## What Gets Installed

This repository is configured as a Gemini CLI extension with:

- **Extension Name**: `vibe-prospecting`
- **MCP Server**: Connects to `https://mcp-ext.vibeprospecting.ai/mcp`
- **Authentication**: OAuth flow via `mcp-remote`
- **Context**: Business data capabilities documentation in `GEMINI.md`

## Files

The extension consists of these files in the repository root:

- `gemini-extension.json` - Extension manifest
- `GEMINI.md` - Context documentation for AI
- `package.json` - Node.js dependencies (includes mcp-remote)

## Authentication

On first use, the extension will:
1. Open your browser for OAuth authentication
2. Prompt you to log in to Vibe Prospecting
3. Store credentials in `~/.mcp-auth`

To reset authentication:

```bash
rm -rf ~/.mcp-auth
```

## Development

For local development:

```bash
git clone https://github.com/explorium-ai/mcp-explorium.git
cd mcp-explorium
gemini extensions link .
```

Changes to the extension files will be reflected immediately without needing to update.

## Uninstall

```bash
gemini extensions uninstall vibe-prospecting
```

## Documentation

- Main README: [README.md](README.md)
- Extension Context: [GEMINI.md](GEMINI.md)
- API Docs: https://developers.explorium.ai/mcp-docs/vibeprospecting
- Homepage: https://www.vibeprospecting.ai

## Support

- Email: support@vibeprospecting.ai
- Contact: https://www.vibeprospecting.ai/contact-us
