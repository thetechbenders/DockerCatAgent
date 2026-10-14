# Installation and operation

Linux Docker Engine with Compose v2 is the reference environment. Support AMD64 and ARM64 subject to actual build verification and the current Claude Code distribution. Ensure outbound HTTPS, adequate disk space and at least the memory recommended by Anthropic.

## Intended CLI flow
1. Clone the entire repository so Docker COPY instructions have their dependencies.
2. Copy .env.example to a private .env; configure resource limits and the stable/latest Claude channel.
3. Run docker compose config, docker compose build --pull, then docker compose up -d.
4. Enter via docker compose exec -u dev agent bash.
5. Verify claude --version, git --version and tmux -V, then authenticate interactively with a supported Claude subscription or Console/API flow.
6. Work in /workspace; use tmux new-session -A -s work to detach/rejoin.

Persist both /workspace and /home/dev. The latter contains Claude authentication and user-local configuration, including .claude.json and .claude. Removing volumes erases that state. docker compose down preserves volumes; docker compose down -v intentionally destroys them. A container restart terminates tmux and active agent commands.

## Rebuild and update
Rebuild from the complete context and run docker compose up -d --force-recreate. Anthropic's stable signed Debian repository is the proposed default and latest an explicit option. Channels move: record actual Claude version, image digest and package state to reproduce a deployment.

## Portainer
Build the image from a full Git checkout on the **same Docker endpoint** as Portainer, then deploy a Compose stack referring to that local image. Do not paste the Dockerfile alone into Portainer: its COPY directives require supporting scripts. If Portainer Git-stack builds are used instead, verify complete build-context support for the actual Portainer version.

## State acceptance
Create one file in /workspace and another in /home/dev. Recreate the container without deleting volumes. Check both survive; separately verify processes did **not** survive. Authenticating Claude and Mem is a manual test, not a CI secret-injection requirement.