# DockerCatAgent documentation

DockerCatAgent is a self-hosted Claude Code terminal environment with persistent home/workspace and optional SSH, vault and MCP access. The foundation is under review; there is no published release, registry image or production approval.

These pages are **reviewable wiki source**. GitHub Wiki was enabled with a placeholder Home when inspected on 2026-10-14; this prepared navigation set was not published during the audit. See the [synchronization procedure](../docs/wiki-publishing.md). The [repository guides](../docs/README.md) are the canonical instructions, and current [audit evidence](../docs/foundation-audit.md) separates implemented behavior from pending acceptance.

## Start here

1. Read [Getting Started](Getting-Started.md) for requirements, full-context installation, authentication and a first session.
2. Review [Architecture](Architecture.md) and [Security](Security.md) before granting filesystem or account access.
3. Choose [Remote Operation](Remote-Operation.md) and [Integrations](Integrations.md) only if those optional features are needed.
4. Use [Maintenance and Recovery](Operations.md) for updates, volume safety, logs and troubleshooting.

## Documentation map

| Section | Topics |
| --- | --- |
| [Getting Started](Getting-Started.md) | Introduction, requirements, installation, login, first Claude session, image updates |
| [Architecture](Architecture.md) | Image, Compose overlays, persistent volumes, runtime identities, filesystem/network boundaries, authentication lifecycle |
| [Remote Operation](Remote-Operation.md) | SSH keys/host identity, localhost/VPN, tmux observation, mobile clients, callbacks, connection failures |
| [Integrations](Integrations.md) | Obsidian mount/write risks, Mem/headless OAuth, tool/account scopes, personal instructions, future MCP recipes |
| [Maintenance](Operations.md) | Rebuild/update, state, draft backup/restore, resource limits, diagnostics, upgrade/recovery |
| [Development](Development.md) | Source layout, build, CI/tests, local acceptance, contribution, security reports, decisions |
| [Security](Security.md) | Threat model, credentials, privileges, disclosure and residual risk |
| [Roadmap](Roadmap.md) | Milestones, dependencies, foundation gates, exploratory work and non-goals |

## Status and evidence

A successful version check or CI build does not validate a real Claude/Mem account, ARM64 hardware, Portainer deployment, remote mobile client or recovery of credentials. Use the [acceptance matrix](../docs/validation.md), [GitHub issues](https://github.com/thetechbenders/DockerCatAgent/issues) and the draft [foundation PR](https://github.com/thetechbenders/DockerCatAgent/pull/1) for the exact scope.

No license has been selected. Owners must approve licensing and any later release/distribution. See [contributing](../CONTRIBUTING.md) and [private security reporting](../SECURITY.md).
