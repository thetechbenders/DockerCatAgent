# Connection and operation troubleshooting

Collect [minimal redacted diagnostics](diagnostics.md) and inspect the [audit evidence](foundation-audit.md) before changing settings. Keep the code SHA, architecture, Docker/Compose and Claude versions, selected overlays, and exact failing step.

| Problem | Likely boundary and next check |
| --- | --- |
| Docker/Compose unavailable | Install or repair host Docker Engine and Compose v2; the image does not include Docker-in-Docker |
| Build cannot fetch packages | Confirm outbound HTTPS, system time and trusted CA chain; keep TLS verification enabled and do not use a third-party Claude binary |
| Signing-key check fails | Stop; verify the upstream published fingerprint and repository before a reviewed change |
| Claude missing or wrong version | Check the actual image/container ID and chosen channel, then rebuild the full context |
| Container is healthy but Claude login fails | Health tests command availability, not provider access or account authorization |
| `/workspace` or home permission denied | Confirm `dev` UID/GID 1000 and the specific volume ownership; avoid broad host permissions |
| SSH not reachable remotely | Loopback is the default; confirm selected trusted interface, VPN route and host firewall |
| Public-key login denied | Check the existing nonempty key file, strict ownership/mode, selected client key, user `dev` and effective server config |
| SSH host identity changed | Verify actual persistent host key and selected project/endpoint privately before editing `known_hosts` |
| Forwarding prohibited | Only the configured local OAuth callback destination is permitted; this is intentional |
| OAuth callback fails | Match client callback, `.env` port and `-L` destination; keep the tunnel open and confirm provider redirect compatibility |
| Mem configured but unauthenticated | Use `/mcp` privately; configuration is not a completed grant or successful request |
| Vault missing | Confirm optional overlay, an existing directory on the Docker host and UID/GID traversal/read access |
| Vault write denied | Read-only is intentional with `compose.obsidian.yml`; use a disposable fixture to verify mode |
| tmux/session disappeared | Restart/recreation kills processes; files persist only if the same volumes are retained |
| Workspace/home appears empty | Verify endpoint/project/volume names and any prior `down -v`; preserve evidence before creating replacement state |
| Update breaks state | Preserve the old image and pre-update backup; rollback has no automatic configuration downgrade |
| Process killed or unable to fork | Inspect memory/PID limits and host pressure before raising limits |

See [remote operation](remote-access.md), [maintenance and recovery](maintenance.md), [Mem](mem-integration.md) and [Obsidian](obsidian-integration.md) for the matching procedure. Account-dependent failure and untested host behavior should remain explicit manual validation work, not a fabricated passed test.
