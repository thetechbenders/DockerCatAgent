# Security

Read the complete [security model](../docs/security.md) before granting access. Report sensitive problems through the [private reporting policy](../SECURITY.md), without credentials or exploit details in public issues.

| Asset or boundary | What to understand |
| --- | --- |
| Workspace and persistent home | Source, prompts, user configuration and authentication can be sensitive |
| Base identity and container controls | Non-root account, dropped capabilities, no-new-privileges, no default ports |
| SSH opt-in | Root daemon and additional capabilities; trusted public keys and persistent host identity |
| Callback forwarding | Restricted destination, not general SSH proxy access |
| Obsidian | Read-only limits writes but not disclosure |
| MCP grants | Tool approval/instructions do not revoke upstream scopes |
| Backups | Can contain account credentials and private host keys; use protected encrypted storage |
| Updates | Signed packages still have mutable dependency/version and vulnerability risks |

Agent commands have the permissions of the runtime/account. Prompt text, personal instructions and tmux observation are not isolation boundaries. Docker administrators can read container volumes and state. No outbound application allowlist, malicious-code certification or automatic compromise recovery is implemented.

Use [validation](../docs/validation.md) and [foundation audit](../docs/foundation-audit.md) to distinguish static assertions, synthetic runtime evidence and outstanding account/host acceptance. For safe evidence collection use [diagnostics](../docs/diagnostics.md).

[Documentation home](Home.md).
