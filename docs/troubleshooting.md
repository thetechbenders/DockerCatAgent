# Troubleshooting

- No Compose or Docker binary: install Docker Engine and Compose v2 on the Linux host; no Docker-in-Docker mode is provided.
- Build failure: check signed Anthropic Debian repository connectivity and verification, not arbitrary third-party binaries.
- Claude missing: rebuild and inspect the actual package channel/version.
- Permission denied: check the development user's UID/GID 1000 and relevant volume ownership; avoid granting unrestricted host access.
- SSH failure: confirm public keys, authorized_keys file ownership/permissions, private/VPN bind address, server host key identity and effective sshd settings.
- OAuth callback failure: ensure the SSH -L destination port matches the configured callback and the local browser tunnel remains active.
- Mem disconnected: configuration is not authentication; use /mcp and review actual OAuth state privately.
- Vault missing or read-only: verify the optional overlay and host file permissions. Read-only is intentional in the default opt-in.
- Session disappeared: tmux processes do not survive a container restart; named volumes preserve files, not processes.
- State lost: confirm Compose project/volume names and whether destructive -v cleanup was run. Restore only from verified backups.