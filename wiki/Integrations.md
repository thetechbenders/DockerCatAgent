# Integrations

All knowledge integrations are optional. Nothing automatically imports vaults or remote notes. See the [integration guide](../docs/integrations.md) for permission and disclosure boundaries.

| Topic | Canonical guide |
| --- | --- |
| Existing Obsidian directory mounted at `/vault` | [Read-only vault setup](../docs/obsidian-integration.md#read-only-access) |
| Deliberate write access and host/sync risks | [Write opt-in](../docs/obsidian-integration.md#write-access-is-a-separate-opt-in) |
| Private data, attachments and task boundaries | [Vault privacy](../docs/obsidian-integration.md#privacy-and-task-boundaries) |
| User-local remote Mem setup | [Mem configuration](../docs/mem-integration.md#user-local-configuration) |
| Browser/headless authentication | [Mem OAuth](../docs/mem-integration.md#browser-and-headless-oauth) and [SSH callbacks](../docs/remote-access.md#restricted-oauth-callback-forwarding) |
| Tool approval versus actual account grants | [Permission scopes](../docs/integrations.md#mcp-tool-permissions-and-account-scopes) |
| Private `~/.claude/CLAUDE.md` | [Personal instructions](../docs/personal-instructions.md) |
| Future remote-provider recipes | [Recipe acceptance](../docs/integrations.md#a-future-mcp-recipe-must-include) |

A read-only filesystem mount prevents writes but permits reading and possible external disclosure. A read-only prompt does not remove a write-capable OAuth grant. Review real provider/tool scopes, minimize mounted paths and revoke unused grants at the provider.

No personal note IDs, private standing orders, account data or sample credentials are distributed. Live Mem OAuth and the user's actual vault remain distinct acceptance scenarios from synthetic tests.

Next: [Security](Security.md), [Architecture](Architecture.md). [Documentation home](Home.md).
