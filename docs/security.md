# Security design and residual risk

The default installation must run an interactive non-root account, publish no ports, mount no host Docker socket, avoid privileged/host namespaces, and bind only its own named volumes. Keep resource limits configurable.

SSH access is opt-in, key-only and loopback-bound on the host by default. Password and root login are prohibited; prefer a VPN over public router port forwarding. The service must persist host keys across normal container recreation. Restrict SSH local forwarding to a user-configured OAuth callback port; disable general remote/agent/X11 forwarding. Test the **effective** sshd configuration and an actual connection, not only template text.

Home/workspace volumes can contain source and secrets. Never log passwords, tokens, OAuth callback query strings or private key contents. Protect volume backups and understand that recreating a container preserves files but kills processes.

Optional Obsidian read access is not authorization to disclose its contents. Its filesystem mount defaults to read-only; modifying the vault requires an explicit writable override. Optional Mem MCP may receive broader OAuth scopes than 'read only'; tool filtering or prompting does not revoke account-scoped rights.

Agent instructions and shell commands are not security boundaries. Container isolation is not absolute, and outbound egress is not fully restricted in this initial architecture. Signed upstream package repositories reduce some supply-chain risk but mutable release channels are not fully reproducible. Record actual image digests and installed versions when assessing a build.