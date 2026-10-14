# DockerCatAgent roadmap

This is a directional roadmap, not a release commitment. Stages are named capability goals; no arbitrary version or release date is implied.

## Foundation (active)
**Goal:** a usable, containerized Claude Code CLI with isolated writable workspace and persistent account state.

- Debian-based Dockerfile using Anthropic's signed stable package channel.
- Compose as source of truth; Portainer image-build instructions.
- Non-root interactive user, tmux, Git, shell utilities and baseline toolchain.
- Persistent home including Claude authentication and MCP state; persistent workspace.
- Configurable resource limits; health and smoke checks.
- Optional key-only SSH mode with loopback host binding, persistent host keys, limited local OAuth port forwarding.
- Optional Obsidian read-only mount with documented write opt-in.
- Optional Mem remote HTTP MCP with user-local OAuth and no automatic note ingestion.
- CI: static configuration, build, persistence, and realistic smoke checks.

**Acceptance gate:** clean image build, executable/version checks, workspace/home write and persistence tests, SSH control validation if enabled, optional overlay validation, accurate documentation, and manual login tests by an account holder. Green synthetic checks do not prove real OAuth or host deployment.

## Access & reliability (next)
- Recovery playbooks for persistent home/workspace and SSH host identity.
- Negative SSH forwarding/authentication regression tests and remote client matrix.
- Documented upgrade/rollback with state-safe migrations.
- Multi-architecture smoke builds where runner availability permits.
- Supply-chain provenance, fixed dependency digest evaluation, SBOM and vulnerability triage.

## Developer experience (candidate)
- Read-only preflight diagnostics that redact secrets.
- Optional language/toolchain profiles instead of bloating the base image.
- Portable SSH client recipes (laptop, tablet, phone).
- Obsidian access-check tooling and path diagnostics.
- Mem OAuth compatibility verification recipes.
- Published documentation/wiki navigation and troubleshooting recipes.

## Exploration (uncommitted)
- Alternative coding agent adapters, not multi-agent orchestration.
- Devcontainer / IDE remote tooling.
- Distribution through a container registry after explicit release approval.
- User-defined instruction presets, with no bundled persona.
- Optional privacy-preserving operational metrics, never automatic prompt/source upload.

## Boundaries
No Kubernetes, Swarm, hosted account provisioning, arbitrary hardware access, automatic infra deployment, web dashboard, privileged host controls, public SSH exposure, or forced external knowledge integration in the foundation.

## Decision history
- 2026-10-14: Generic product, Claude Code first, Compose authoritative.
- 2026-10-14: SSH, Obsidian and Mem explicitly optional. SSH host published loopback only by default.
- 2026-10-14: No third-party agent binary and no bundled private persona.
- 2026-10-14: License awaits an owner decision; do not invent one.
- 2026-10-14: Build, test, review and branch discipline precede merging or releasing.