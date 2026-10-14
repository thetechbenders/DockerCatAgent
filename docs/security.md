# Security model and residual risk

The foundation is an interactive environment capable of executing code and making outbound requests. Protect source, account state, SSH identity and optional knowledge sources. It is not a hardened sandbox for arbitrary hostile code.

## Baseline boundary

The base uses non-root `dev` (UID/GID 1000), drops Linux capabilities, enables `no-new-privileges`, publishes no ports and mounts only its dedicated home/workspace volumes. It does not mount a Docker socket, run privileged, share host namespaces or expose an HTTP service. Resource limits reduce some accidental host exhaustion; they do not guarantee availability under every workload.

Docker administrators can inspect all container files, credentials and processes. Do not run the environment on an untrusted Docker host. Do not mount an entire host home, add host device access or relax isolation as a troubleshooting shortcut. Container isolation has kernel/runtime limits and does not prevent all escape or exfiltration.

## Optional SSH boundary

SSH is a separate explicit overlay. Its daemon runs as root inside the container and receives additional capabilities; authenticated shells run as `dev`. Key-only login, root/password/keyboard-interactive restrictions, strict key-file checks and persistent Ed25519 host keys need effective-config and actual connection tests.

The host binding defaults to loopback. Prefer a controlled private/VPN interface for remote access and enforce host/network policy separately. Only local TCP forwarding to the configured loopback OAuth callback destination is allowed. Remote, agent, X11, Unix-socket and tunnel forwarding are disabled. This does not create a restricted shell or a read-only observer account. See [remote operation](remote-access.md).

## Credentials and data

The home volume can hold Claude credentials, user configuration and MCP grants. Workspace may contain secrets from checked-out projects. Backups can copy these secrets and SSH private host keys; use protected encrypted storage and a verified restore process. Never commit credentials, copy personal config into image layers, inject real account secrets into CI or publish raw support logs.

Read-only vault mounts prevent filesystem writes, not reading or external disclosure. Mem/provider OAuth scopes may grant writes even if tool instructions ask for read-only access. Tool approval, account grants and filesystem permissions are independent controls. Minimize provider scopes and mounted paths; revoke unused grants through the provider.

Treat repository instructions, vault text and MCP responses as untrusted task input. Prompts, personal instructions and tmux read-only attachment are not security boundaries. Review requested tool actions and changes with the consequences of the existing account permissions in mind.

## Network and supply chain

Ordinary outbound networking is available; no application egress allowlist is implemented. Bind ports deliberately and evaluate data sent to Claude and optional providers. VPN software, host firewalls and endpoint access management are operator responsibilities.

Claude packages use the upstream signed repository with a pinned signing-key fingerprint. Moving base/dependency channels remain a reproducibility limitation; signatures are not a guarantee of bug-free packages or complete provenance. Keep TLS verification enabled. Build-network CA/proxy settings must not become baked-in runtime credentials.

## Security acceptance and reporting

Static assertions detect selected source mistakes. Synthetic tests exercise disposable identities, files and network behavior. They do not prove real account permissions, production host security, mobile trust or recovery from compromise. See [validation](validation.md) and the [foundation audit](foundation-audit.md).

Report sensitive defects through the [security reporting policy](../SECURITY.md). There is no claimed certification, penetration-test completion or response-time guarantee. No software license, release or production approval is implied by green CI.
