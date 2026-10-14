# Remote Operation

The [remote access guide](../docs/remote-access.md) is the authoritative procedure. The base container exposes no ports; SSH requires its explicit overlay and a protected, existing public-key file. Never put client private keys in the image or repository.

| Task | Guide |
| --- | --- |
| Enable key-only SSH and loopback binding | [Authorized keys](../docs/remote-access.md#authorized-keys-and-loopback-binding) |
| Verify server fingerprint and understand key rotation | [Host identity](../docs/remote-access.md#host-identity-and-key-changes) |
| Reach a trusted VPN/private interface | [Remote clients](../docs/remote-access.md#vpn-and-remote-clients) |
| Rejoin work and observe a session | [tmux](../docs/remote-access.md#tmux-and-observation) |
| Forward an OAuth callback safely | [Restricted forwarding](../docs/remote-access.md#restricted-oauth-callback-forwarding) |
| Inspect effective server settings | [Effective configuration](../docs/remote-access.md#effective-configuration-and-troubleshooting) |
| Diagnose connection problems privately | [Troubleshooting](../docs/troubleshooting.md) and [diagnostics](../docs/diagnostics.md) |

Phone/tablet use requires a protected SSH key, trusted host fingerprint, a private network path and a workable terminal/tmux keyboard. The project does not supply a VPN, mobile app or certified client matrix.

Read-only tmux attachment limits input through that client, but a shared `dev` shell is fully capable of modifying files and reading account state. It is not a viewer authorization role.

Only the selected loopback callback destination is permitted. A local SSH listener is not proof of a completed OAuth flow. [Mem](../docs/mem-integration.md) describes the supported setup and outstanding account-holder checks.

Next: [Security](Security.md), [Maintenance](Operations.md). [Documentation home](Home.md).
