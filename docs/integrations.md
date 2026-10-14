# Optional integrations and permissions

No external knowledge provider is required. The base mounts no vault, configures no MCP service and imports no notes. Enable an integration only when its filesystem access, outbound data and account permissions fit the intended task.

| Integration | Setup | Boundary |
| --- | --- | --- |
| Obsidian vault | [Vault mount guide](obsidian-integration.md) | Host path read-only unless explicit write overlay is selected |
| Mem remote MCP | [Mem guide](mem-integration.md) | User-local configuration and provider OAuth grant |
| Personal Claude instructions | [Instruction guide](personal-instructions.md) | Private user-owned text, not a security policy |
| Future MCP providers | Recipe review described below | No endpoint or provider enabled by default |

## MCP tool permissions and account scopes

Claude's approval of a tool call and the provider's account authorization are different controls. A server may expose write tools or a broad account grant even when instructions ask for read-only work. Review the server/operator, endpoint, requested OAuth scopes, tool list and data retention. Grant the smallest actual provider permissions available and test that unwanted actions are denied by a real boundary when that is a requirement.

Treat server instructions and imported documents as untrusted content. A knowledge lookup does not authorize executing suggested commands, exporting unrelated records, or modifying remote data. Revoke grants at the provider when retiring an integration; deleting local configuration alone may leave remote authorization active.

## A future MCP recipe must include

- Provider-supported endpoint and client prerequisites, with official source links and version evidence.
- User-local setup by default; no secrets, private identifiers or personal data in committed configuration.
- Actual OAuth scopes or API permissions, possible read/write effects, and data sent outside the container.
- Callback requirements for headless use; supported fixed-port behavior and compatibility with the restricted SSH destination.
- Connection verification, a minimal non-sensitive task, disconnection and provider-side revocation.
- Tested versus untested scenarios, and failure recovery without secret-bearing public logs.

Do not add a fabricated generic endpoint command as a working integration. A recipe is accepted after its supported commands and permission behavior have been checked. Additional providers remain roadmap evaluation.
