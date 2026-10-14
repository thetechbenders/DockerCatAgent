# Architecture

One Debian container provides one interactive Claude Code environment. Docker Compose owns runtime configuration. There is no HTTP service, orchestration layer or hosted control plane.

| Question | Canonical explanation |
| --- | --- |
| How is Claude installed, and what does health mean? | [Image/process model](../docs/architecture.md#image-and-process-model) |
| Which Compose files are optional? | [Base and overlays](../docs/architecture.md#compose-profiles-and-overlays) |
| Which files survive recreation? | [Storage and identity](../docs/architecture.md#storage-and-identity) |
| What is the runtime user and SSH privilege difference? | [Identity/capability model](../docs/architecture.md#storage-and-identity) |
| How do login, expiry and revocation affect persisted state? | [Authentication lifecycle](../docs/architecture.md#authentication-state-lifecycle) |
| Where are filesystem/network trust boundaries? | [Boundaries](../docs/architecture.md#filesystem-and-network-trust) |
| Why were these choices made? | [Architecture decisions](../docs/architecture-decisions.md) |

The base runs UID/GID 1000 and publishes no ports. SSH explicitly adds a root daemon while keeping `dev` login shells; its own host-key volume persists server identity. Vault access is absent by default and read-only when that overlay is selected. Mem remains user-local and optional.

Preserving home files does not guarantee provider authorization remains valid. Read-only mounts do not prevent data disclosure. Use [Security](Security.md) for the consequences and [Maintenance](Operations.md) for updates/recovery.

[Documentation home](Home.md).
