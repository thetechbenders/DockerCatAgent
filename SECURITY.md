# Security and vulnerability reporting

DockerCatAgent is pre-release; the foundation source is merged into `main`. No stable release series or security response-time guarantee exists. There is no supported production release.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/thetechbenders/DockerCatAgent/security/advisories/new) if the repository enables it. If that option is unavailable, contact a Techbenders maintainer through an established private channel before sharing details. This policy does not claim that private reporting is enabled or invent an unverified contact address.

Include the affected source commit, sanitized environment, reproduction steps, impact, and any proposed fix. Do not place exploit details, credentials, private keys, OAuth callback URLs, account identifiers, or vault contents in public issues. Ordinary sanitized configuration or usability reports can use the bug template; disclose potentially exploitable weaknesses privately first.

## Runtime boundaries

The default Compose service runs as the non-root `dev` user, drops Linux capabilities, and publishes no ports. It does not mount the host Docker socket, use privileged mode, or share the host network namespace. The optional SSH overlay has a different privilege model: sshd runs as root inside the container to authenticate and switch sessions to `dev`. Public-key-only authentication, disabled root/password login, and restricted local forwarding must hold in the effective configuration.

Loopback is the default SSH host binding. Operators choosing another interface must assess exposure and their VPN/firewall controls. SSH credentials grant an interactive shell; read-only tmux attachment is a viewing convenience, not a separate authorization role.

The workspace and full user home persist and can contain code, Claude configuration/authentication, MCP state, and other secrets. Docker administrators can inspect these volumes. Protect backups, avoid secret-bearing diagnostics, and understand that deleting a volume deletes account state. Recreating a container preserves its volumes but ends active processes.

Read-only Obsidian mounting prevents writes to the vault; it does not prevent the agent from reading or sending allowed data to an external provider. Mem is optional and account-authorized. Instructions and tool filters do not revoke upstream OAuth scopes. Neither personal `CLAUDE.md` instructions nor a persona is a security boundary.

## Known limits

Container isolation is not absolute, and this foundation does not enforce an outbound network allowlist. Dependencies and upstream channels can move between builds; signed package installation is separate from reproducibility and vulnerability freedom. Real OAuth, host/client compatibility, recovery procedures, and hardware acceptance have independent evidence requirements.

See the [security design](docs/security.md), [foundation audit](docs/foundation-audit.md), [validation guide](docs/validation.md), and [roadmap](ROADMAP.md) for the implementation, test disposition, and remaining work.
