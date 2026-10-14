# Architecture

## Baseline runtime
One Debian-based container hosts Claude Code CLI, Git, shell tools and tmux. Docker Compose defines runtime configuration and two named volumes: a development workspace and the non-root user's home directory. Home persistence is important because Claude uses both its .claude directory and .claude.json file for login, project trust, MCP and session settings. The base service stays alive for exec/terminal access, with no network ports published.

## Optional boundaries
SSH is a separate Compose overlay, not part of default exposure. A root-owned daemon may be required to authenticate keys and drop privileges to the dev user. Host key identity persists independently. Local port forwarding is limited to an explicit OAuth callback destination. Read-only tmux attachment is a viewer convenience, not permission isolation.

Obsidian is a host-path Markdown vault bind mount, absent by default and read-only when enabled. Write mode requires a separate explicit overlay. Mem is a user-configured remote HTTPS MCP service. Its OAuth credentials remain in the persistent user home, not project source control.

## Threat model
The agent can execute code and access permitted container files and network services. A read-only mount prevents writes, not information disclosure. Docker administrators can inspect named volumes and container state. OAuth scopes and MCP tool restrictions are separate. The security boundary is the actual runtime and provider authorization, never a personality prompt.

## Portainer
The build context must include Dockerfile, scripts and configuration. A pasted Dockerfile with missing COPY inputs is not a functional deployment. Build from a full Git checkout or deploy a prebuilt image on the same Docker endpoint.