# Optional Mem MCP

Mem is never mandatory. Its remote MCP endpoint is https://mcp.mem.ai/mcp. Add a **user-local** HTTP MCP connection with Claude Code's supported commands, not a committed project .mcp.json.

Example command inside the container:

claude mcp add --transport http --scope user --callback-port 8765 mem https://mcp.mem.ai/mcp

Then enter Claude Code, run /mcp, and complete the provider's browser-based OAuth flow. For a headless session, keep a restricted SSH local-forward active at the selected callback port. Verify the connection with claude mcp get mem or /mcp; avoid printing tokens, private note bodies and callback URLs.

A user's OAuth grants may permit writes even when instructions request read-only behavior. A prompt or tool filter does not cancel upstream scopes. Do not automatically ingest all Mem notes. Users choose their own collections, identifiers and standing orders. Authentication state stays in the persistent user home and never in the public repository.