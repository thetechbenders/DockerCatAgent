# DockerCatAgent documentation

DockerCatAgent is a self-hosted Claude Code terminal environment with persistent home/workspace and optional SSH, vault and MCP access. The foundation source is on `main` following [PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1), but there is no published release, registry image or production approval.

These navigation pages are maintained as reviewed source in the repository and published separately under the [synchronization procedure](../docs/wiki-publishing.md). The [repository guides](../docs/README.md) remain canonical, and [validation evidence](../docs/validation.md) separates implemented features from pending account and host acceptance.

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

A successful version check or CI build does not validate a real Claude/Mem account, ARM64 hardware, Portainer deployment, remote mobile client or recovery of credentials. Use the [acceptance matrix](../docs/validation.md), [GitHub issues](https://github.com/thetechbenders/DockerCatAgent/issues) and the merged [foundation PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1) for implementation history and the remaining acceptance scope.

No license has been selected. Owners must approve licensing and any later release/distribution. See [contributing](../CONTRIBUTING.md) and [private security reporting](../SECURITY.md).
