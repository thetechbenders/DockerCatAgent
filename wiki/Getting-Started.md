# Getting Started

The [installation guide](../docs/installation.md) is the complete procedure. The image supplies Claude Code, Git, shell tools and tmux; you supply a Docker host and your own authorized account. No provider account or personal configuration is bundled.

| Step | Canonical guide |
| --- | --- |
| Requirements and host/architecture limits | [Requirements](../docs/installation.md#requirements) |
| Clone the foundation branch and build all COPY inputs | [Full build context](../docs/installation.md#obtain-the-full-build-context) |
| First-run authentication and a minimal session | [First session](../docs/installation.md#first-run-authentication-and-a-first-session) |
| Safe stop/down and persistence | [State safety](../docs/installation.md#persistence-and-safe-shutdown) |
| Portainer's endpoint-local image/full context | [Portainer](../docs/installation.md#portainer) |
| Rebuilding and updating | [Maintenance](../docs/maintenance.md#rebuilding-and-updating) |

Work in `/workspace` as `dev`; the entire `/home/dev` persists user-local Claude and MCP state. A container recreation ends running processes and tmux even when the files survive. Never use `down -v` for a routine update.

`claude --version` proves executable availability. A consenting account holder must complete the supported login flow and a real task before declaring authentication accepted. Headless MCP callbacks are covered separately in [Remote Operation](Remote-Operation.md).

Next: [Architecture](Architecture.md), [Security](Security.md), [Integrations](Integrations.md). [Documentation home](Home.md).
