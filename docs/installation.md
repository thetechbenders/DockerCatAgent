# Installation and first session

DockerCatAgent is a foundation under review, not a published image or production release. Use the [active draft PR](https://github.com/thetechbenders/DockerCatAgent/pull/1) and [validation guide](validation.md) to distinguish build evidence from host and account acceptance.

## Requirements

- A Linux Docker Engine host with Docker Compose v2 and permission to manage containers. Docker administrators can read container state and volumes.
- Outbound HTTPS to Debian and Anthropic during builds, and to the services you choose at runtime.
- Disk for the image, workspace, persistent home and backups. The default Compose limits are 4 GiB memory, 2 CPUs and 512 processes; these are configurable limits, not measured minimums.
- Your own supported Claude account or provider-approved authentication method for live sessions. Accounts and credentials are not bundled.

AMD64 build evidence does not establish ARM64 hardware support. See [ARM64 acceptance issue #2](https://github.com/thetechbenders/DockerCatAgent/issues/2). Other hosts and Portainer versions require their own acceptance record.

## Obtain the full build context

Until PR #1 is reviewed and merged, the foundation is on its feature branch. On the Docker host:

```sh
git clone --branch feat/claude-docker-foundation https://github.com/thetechbenders/DockerCatAgent.git
cd DockerCatAgent
cp .env.example .env
docker compose version
docker compose config -q
docker compose build --pull
docker compose up -d
docker compose ps
docker compose exec -u dev agent bash
```

Keep `.env` private. It selects resource limits, package channel and optional mount/network settings; it is not a place for account tokens. The Dockerfile copies `scripts/` and `config/`, so a standalone pasted Dockerfile is insufficient.

The package channel defaults to `stable`; `latest` is an explicit choice. Both move over time. A successful rebuild may install a different Claude version. See [updates and recovery](maintenance.md).

## First-run authentication and a first session

Inside the container:

```sh
id
claude --version
git --version
tmux -V
cd /workspace
tmux new-session -A -s work
claude
```

When using the optional SSH Compose override, specify `-u dev` explicitly for ordinary `docker compose exec` commands; otherwise its root-running daemon profile can create root-owned files in persistent user state. The interactive shell should run as `dev` (UID/GID 1000), with writable `/workspace` and `/home/dev`. Follow Claude's displayed login instructions for your chosen account. Use [Anthropic's current setup guidance](https://code.claude.com/docs/en/setup) rather than pasting credentials into commands or issues. First-run trust prompts apply to the directory you enter; inspect a repository before granting trust.

For a first task, use a disposable repository or ask Claude to explain files in an empty workspace. Review requested tool permissions and generated changes before applying them. No real login or prompt response is implied by `claude --version` passing.

Detach tmux with `Ctrl-b`, then `d`. Reconnect with the same tmux command. Restarting or recreating the container ends tmux and active commands; it preserves files when the same volumes are retained.

Headless MCP OAuth has a separate callback flow; see [Mem](mem-integration.md) and [remote access](remote-access.md). The SSH callback setting does not automatically configure or validate Claude account login.

## Persistence and safe shutdown

The Compose service mounts named volumes at `/workspace` and the **entire** `/home/dev`. Claude state can include `.claude/` and `.claude.json`; its exact files depend on the installed version. Persisting home avoids assuming that one token file contains all necessary state. Tokens can still expire or be revoked externally.

```sh
docker compose stop
docker compose start
docker compose down
```

`docker compose down` removes the container and network while retaining named volumes. **`docker compose down -v` destroys the project's named volumes**, including workspace and authentication state. Do not use it for routine updates. Changing the Compose project name or Docker endpoint can select different volumes; an apparently empty home may be the wrong project rather than data loss.

Run [synthetic persistence checks](validation.md) before authenticating, then account-holder checks afterward. File survival and live account authentication are different acceptance gates.

## Portainer

Portainer's Docker endpoint must have the image locally. Build from a complete checkout on that same endpoint:

```sh
docker build --pull -t dockercatagent:local .
```

Then use [`compose.portainer.yml`](../compose.portainer.yml) as an image-only stack definition. The file is the base profile; it does not activate SSH or a vault. Review the resulting project and volume names before migrating existing data. A different stack name can create new empty volumes.

If using a Portainer Git-stack build feature, first confirm that your Portainer version supports the complete repository context and the required build mode. This guide does not claim a tested Portainer deployment.

Next: [architecture](architecture.md), [remote operation](remote-access.md), [integrations](integrations.md), and [maintenance](maintenance.md).
