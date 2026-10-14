# Documentation guide

The guides in `docs/` are the canonical operator and development documentation, reviewed with code. The [official GitHub Wiki](https://github.com/thetechbenders/DockerCatAgent/wiki) publishes concise navigation from [`wiki/`](../wiki/Home.md), with canonical guide links pinned to its reviewed source commit. See [publication evidence and the update procedure](wiki-publishing.md); subsequent source edits require another reviewed synchronization.

| Reader goal | Guide |
| --- | --- |
| Requirements, installation, first authentication and session | [Installation](installation.md) |
| Container design, overlays, identities and storage | [Architecture](architecture.md) |
| SSH, keys, VPN/loopback, tmux, mobile and callbacks | [Remote operation](remote-access.md) |
| Optional knowledge providers and permission boundaries | [Integrations](integrations.md) |
| Vault mount modes and host permissions | [Obsidian](obsidian-integration.md) |
| User-local Mem configuration and headless OAuth | [Mem](mem-integration.md) |
| User-local Claude instructions without private repository samples | [Personal instructions](personal-instructions.md) |
| Updates, persistence, resource limits and recovery | [Maintenance](maintenance.md) |
| Privacy-preserving logs and problem diagnosis | [Diagnostics](diagnostics.md) and [troubleshooting](troubleshooting.md) |
| Local development, checks and source layout | [Development](development.md) |
| Acceptance matrix and manual checks | [Validation](validation.md) |
| Threat model and residual risks | [Security](security.md) |
| Design decisions and unresolved choices | [Architecture decisions](architecture-decisions.md) |
| Publishing prepared wiki pages after review | [Wiki publishing](wiki-publishing.md) |
| Repository issues, labels and milestones | [GitHub management](github-management.md) |
| Scoped audit findings and evidence | [Foundation audit](foundation-audit.md) |

The [roadmap](../ROADMAP.md), [contribution guide](../CONTRIBUTING.md) and [security reporting policy](../SECURITY.md) describe project direction and participation. For a problem report, state the code SHA, Docker/Compose and Claude versions, host architecture and selected overlays. Share redacted evidence, not authentication files.

## Reading validation claims

- **Implemented** means code or configuration exists; it is not a release claim.
- **Static check** means source/configuration was inspected or parsed.
- **Synthetic runtime check** means a disposable test exercised the image without real account credentials.
- **Manual acceptance** means a named host/account scenario was actually exercised and recorded.
- **Deployment** requires a real operational environment; CI does not establish one.

Read exact-head CI and the audit record for scoped evidence; the audit includes historical runs from before the independent SSH remediation. No release, registry image or production deployment is implied by this documentation.
