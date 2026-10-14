# DockerCatAgent

**Portable, self-hosted Claude Code CLI development environments.**

A Docker/Compose toolkit for running Claude Code with a persistent workspace, terminal sessions, optional key-only SSH access, and optional Obsidian/Mem integrations. Designed for ordinary Linux AMD64/ARM64 Docker hosts, not a particular NAS, network, or user.

> **Status: foundation under development.** The feature branch is not a released or production-validated environment. Docker/SSH/OAuth validation results must be reported before calling it ready.

## Core promises
- Docker Compose is authoritative; Portainer is supported through a complete repository build context or a locally prebuilt image.
- Claude Code comes from an Anthropic-supported distribution, never a third-party repackaged binary.
- Non-root interactive development account and persistent workspace/user state.
- Optional SSH with public-key authentication, localhost default, VPN recommendation, and narrowly restricted OAuth forwarding.
- Optional read-only Obsidian vault mounts; write access requires explicit opt-in.
- Optional remote Mem MCP; users configure and authorize their own account, with no bundled personal notes.
- No public network exposure, Docker socket, privileged container, or broad host mount by default.

## Navigation
- [Roadmap and delivery stages](ROADMAP.md)
- [Architecture and decisions](docs/architecture.md)
- [Security and privacy model](docs/security.md)
- [Installation and operational design](docs/installation.md)
- [Remote access and tmux](docs/remote-access.md)
- [Obsidian integration](docs/obsidian-integration.md)
- [Mem MCP integration](docs/mem-integration.md)
- [Wiki publishing plan](wiki/Home.md)
- [Contribution guide](CONTRIBUTING.md)

## Development status
The planning and documentation branch is the working reference while the functional image and tests are being reviewed. Refer to the active pull request and CI evidence for exact capabilities; proposed features are not shipped features.

Techbenders maintains DockerCatAgent. It is independent of Anthropic, Mem, and Obsidian. **No repository license has been chosen**. Public source visibility is not the same as permission to redistribute.