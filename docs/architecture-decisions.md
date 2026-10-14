# Architecture decisions

This log records the current foundation design. New decisions should state the problem, alternatives, chosen boundary, implications and validation evidence in a focused PR. A roadmap candidate is not an accepted architecture change.

| Decision | Current choice | Implication |
| --- | --- | --- |
| Product shape | One self-hosted Claude Code terminal environment | No dashboard, multi-agent orchestration or hosted service |
| Runtime configuration | Docker Compose is authoritative | Portainer uses a complete context or endpoint-local image, with separate host acceptance |
| Claude distribution | Anthropic-supported signed Debian packages | Verify signing key; moving channels still require reproducibility work |
| Default identity | Non-root `dev`, UID/GID 1000 | Workspace/home must be writable; optional host mounts must respect host permissions |
| Persistent state | Entire development home plus workspace | Preserve version-dependent account/config files; treat home as sensitive |
| Remote access | Separate key-only SSH overlay with loopback default | Root daemon surface and restricted forwarding need independent validation |
| Vault access | Absent by default; optional read-only mount | Write mode is a separate deliberate opt-in |
| Remote knowledge | Optional user-local MCP setup | No private notes, automatic ingestion or credentials in source |
| Health | CLI prerequisites rather than HTTP endpoint | Healthy does not prove account, provider, session or data recovery |
| Documentation | Canonical repository guides with navigational wiki pages | Publish only reviewed content and retain a single source of truth |

## Decisions still required

The owners must select and approve a software license. Until then, public visibility is not a redistribution grant. Registry distribution and release policy also require explicit authorization.

Backup encryption/key management, dependency pinning/provenance, configuration migration, alternative coding agents and remote IDE compatibility remain scoped roadmap work. Their inclusion here does not implement or approve them.
