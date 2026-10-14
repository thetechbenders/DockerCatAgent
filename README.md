# DockerCatAgent

**A self-hosted Claude Code terminal environment with persistent files and optional SSH access.**

[![Foundation CI](https://github.com/thetechbenders/DockerCatAgent/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/thetechbenders/DockerCatAgent/actions/workflows/ci.yml?query=branch%3Amain)

DockerCatAgent packages Claude Code, Git, tmux, and common development tools in one Debian-based Docker container. Docker Compose defines a non-root development environment with named volumes for the workspace and user home. SSH, Obsidian vault access, and Mem MCP are optional.

> **Development status:** the foundation source was merged into `main` through [PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1). There is **no approved release, published container image, or production acceptance**. CI only validates its tested commit; it does not prove live account authentication or host deployment.

The current foundation includes:

- Claude Code installation from its upstream signed Debian package channel.
- A `dev` account, persistent `/workspace` and `/home/dev`, configurable resource limits, and a CLI health check.
- No published ports, privileged mode, host Docker socket, or host-directory mounts in the default Compose configuration.
- An optional key-only SSH overlay, a loopback host binding, persistent SSH host keys, and forwarding restricted to a selected OAuth callback destination.
- Separate read-only and explicitly writable Obsidian vault overlays.
- Documentation for user-configured Mem MCP, with no bundled account, notes, or credentials.

Account-backed authentication, ARM64 hardware acceptance, and Portainer deployment remain explicit validation work. See the [foundation audit](docs/foundation-audit.md), [validation guide](docs/validation.md), and [roadmap](ROADMAP.md) for evidence and acceptance gates.

## Try the development foundation

Use a Linux Docker Engine host with Docker Compose v2, outbound HTTPS, and enough disk and memory for your work. AMD64 is the CI reference architecture; ARM64 acceptance is tracked in [#2](https://github.com/thetechbenders/DockerCatAgent/issues/2). You need your own supported Claude account or API access to use Claude Code.

```sh
git clone --branch main https://github.com/thetechbenders/DockerCatAgent.git
cd DockerCatAgent
cp .env.example .env
docker compose config -q
docker compose build --pull
docker compose up -d
docker compose exec -u dev agent bash
```

Inside the container:

```sh
claude --version
git --version
tmux -V
tmux new-session -A -s work
claude
```

Authenticate using Claude Code's interactive flow. Claude account login may use a paste-code browser flow that needs no tunnel. Some optional MCP-provider OAuth flows use a local callback; configure the [restricted SSH forwarding](docs/remote-access.md#restricted-oauth-callback-forwarding) **only when that flow requires it**. Live subscription, API-key, and Mem authentication still require separate account-holder tests.

Work in `/workspace`. Files and account configuration in `/home/dev` persist when the container is recreated with the same Compose project and volumes. Container recreation ends running Claude and tmux processes. `docker compose down` preserves the volumes; **`docker compose down -v` deletes them**, including authentication state. Protect backups of the user home as credential-bearing data.

To rebuild after reviewing source or upstream updates:

```sh
docker compose build --pull
docker compose up -d --force-recreate
```

Record the source commit and installed Claude version when reporting results. Channels and base-image tags can change between builds; bit-for-bit reproducibility is future work. Read the [maintenance guide](docs/maintenance.md) before updating valuable state.

## Documentation

Start with the [documentation index](docs/README.md). The guides cover:

| Task | Guide |
| --- | --- |
| Install, authenticate, and use Portainer with a complete build context | [Installation](docs/installation.md) |
| Understand identities, volumes, filesystem boundaries, and health checks | [Architecture](docs/architecture.md) |
| Configure SSH, callback forwarding, tmux, and remote clients | [Remote operation](docs/remote-access.md) |
| Mount an Obsidian vault safely | [Obsidian](docs/obsidian-integration.md) |
| Configure optional remote Mem MCP | [Mem integration](docs/mem-integration.md) |
| Maintain state, update, and plan recovery | [Maintenance](docs/maintenance.md) |
| Diagnose problems without exposing private data | [Troubleshooting](docs/troubleshooting.md) |
| Build, test, and contribute | [Development](docs/development.md), [contributing](CONTRIBUTING.md) |

The [wiki landing page](wiki/Home.md) is prepared source for a future reviewed GitHub Wiki publication. It links to canonical repository guides; it has not been published separately by this work. See the [publication procedure](docs/wiki-publishing.md).

## Scope and support

DockerCatAgent is a terminal environment, maintained by Techbenders and independent of Anthropic, Mem, and Obsidian. It provides no hosted accounts, web service, orchestration platform, or automatic deployment. Optional integrations use your own accounts and authorization. Container isolation and read-only mounts do not prevent permitted data from being disclosed to an external provider.

Use [issues](https://github.com/thetechbenders/DockerCatAgent/issues) for reproducible defects and scoped proposals. Include sanitized environment details and the source commit; keep secrets and private account data out of reports. Report vulnerabilities through the [security policy](SECURITY.md).

**No software license has been approved.** Public visibility does not grant redistribution rights. The owner decision and third-party notice policy are tracked in [#6](https://github.com/thetechbenders/DockerCatAgent/issues/6).
