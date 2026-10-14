# Optional Mem MCP

Mem is optional. DockerCatAgent does not configure a Mem account, ship note identifiers or automatically ingest collections. Mem's remote HTTP MCP endpoint is `https://mcp.mem.ai/mcp`; users authorize their own account.

## User-local configuration

Enter the running container as `dev`. Check the installed command's options before configuring it:

```sh
claude mcp add --help
claude mcp add --transport http --scope user --callback-port 8765 \
  mem https://mcp.mem.ai/mcp
claude mcp get mem
```

The options, including a fixed OAuth callback port, are described in [Claude's official MCP guide](https://code.claude.com/docs/en/mcp). CLI syntax is distinct from live Mem acceptance. If the installed version does not support an option, stop and resolve version compatibility rather than hand-editing credential files or removing SSH restrictions.

`--scope user` keeps this definition in the persistent user home rather than a committed project `.mcp.json`. Inspect `claude mcp get mem` locally: configuration details or status are not proof of a completed authenticated request and may contain private metadata.

## Browser and headless OAuth

Launch `claude`, use `/mcp`, select the server and follow its authentication prompts. When the browser is on a separate client, first open the [restricted SSH callback tunnel](remote-access.md#restricted-oauth-callback-forwarding) at port 8765. The configured callback port, tunnel destination and `OAUTH_CALLBACK_PORT` must agree. Do not change the grant or redirect URI blindly if the provider rejects the flow.

The user's Claude login and Mem OAuth are separate. A green image build or a displayed server definition cannot validate either. An account holder must confirm OAuth completion, a permitted non-sensitive request, behavior after container recreation, and reauthentication after expiry/revocation. [Issue #21](https://github.com/thetechbenders/DockerCatAgent/issues/21) tracks the narrower live Mem/headless case; use current issue scope as the acceptance source.

## Data and permissions

Review the provider's requested scopes and the tools exposed in `/mcp`. A read-only instruction does not revoke a write-capable grant. Choose one explicitly authorized small query; avoid automatically listing or exporting all private notes. Do not publish provider responses, callback URLs, account metadata or tokens as test evidence.

Authentication and user-local configuration persist through the home volume, subject to provider token lifetime and client version. Losing the volume may require fresh authentication. To retire the local definition:

```sh
claude mcp remove mem --scope user
```

Also revoke the provider-side connection as appropriate; local removal is not a remote revocation guarantee. Follow current provider guidance for deleting obsolete credential state privately. See [integration boundaries](integrations.md), [authentication lifecycle](architecture.md#authentication-state-lifecycle) and [protected backups](maintenance.md#backup-and-restoration-procedure-draft).
