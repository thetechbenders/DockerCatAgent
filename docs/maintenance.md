# Maintenance, persistence and recovery

Use the same Docker endpoint, Compose project name and enabled overlays throughout an operation. The base project's configured name is `dockercatagent`; an explicit `-p`, environment override or Portainer stack can change the volume names. Before changing anything, record the source SHA, image ID, installed Claude version, selected overlays and actual volume names privately.

## Rebuilding and updating

A rebuild updates the image; recreation attaches existing volumes to a new container. Both account state and source files need a protected backup before an update that could change their format. Finish or save active work first: recreation ends tmux and running agent commands.

On the Docker host, after reviewing the intended source revision and validating the backup procedure:

```sh
git rev-parse HEAD
docker compose exec -T -u dev agent claude --version
docker image inspect dockercatagent:local --format '{{.Id}}'
docker compose config -q
docker compose build --pull
docker compose up -d --force-recreate
docker compose exec -T -u dev agent /usr/local/bin/dockercat-smoke
```

These commands are for the base profile. For SSH/vault use, supply the same reviewed `-f` overlay set to every Compose command. Inspect the new container's health and run the matching [acceptance checks](validation.md). Account holders must confirm live login and MCP connections after changes; a version command does not test them.

Keep the previous image identifier and a protected pre-update state backup until acceptance succeeds. Returning to an older image does not undo a newer client's writes to home. No automatic configuration migration, schema downgrade or rollback service exists.

## Build reproducibility

The Debian base tag, Debian repositories and Claude `stable`/`latest` channels can move. Signed package installation is an origin/integrity control; it is not a complete dependency lock. Record the actual code SHA, Docker image ID, Claude version, build date and package inventory locally. A local image ID is not a published registry digest or provenance attestation.

Dependency pinning, SBOM/provenance and supply-chain regression work belong to the [roadmap](../ROADMAP.md). There is no authorized registry image or release at this stage.

## State inventory

With the container running, inspect mount metadata without dumping its environment or file contents:

```sh
docker inspect "$(docker compose ps -q agent)" \
  --format '{{range .Mounts}}{{printf "%s %s -> %s (rw=%t)\n" .Type .Name .Destination .RW}}{{end}}'
```

Preserve the whole home, workspace and, in SSH mode, host-key volume. Authorized public keys and optional vault data are host-managed files outside those named volumes. An Obsidian vault's backup is the host owner's responsibility. Named volumes are not backups: host loss, administrator deletion or `down -v` can destroy them.

## Backup and restoration procedure draft

**Status:** operator procedure design; no credential-safe automated backup/restore tool or real-account recovery has been certified. Do not treat this section as a tested one-command backup. A restore drill with disposable data must establish the selected storage/encryption method before relying on it.

1. Choose an encrypted backup destination, protect its encryption keys separately and restrict access. Workspace, home and SSH host keys can all contain sensitive material. Do not place plaintext archives in the repository, CI artifacts, public storage or shared logs.
2. Inventory the actual volume names, source SHA/image and enabled overlays. Finish active writes and stop the service using that overlay set. Preserve timestamps, ownership, modes and hidden files; partial home copies risk losing authentication/configuration state.
3. Use the Docker host's reviewed backup mechanism to capture the named volumes consistently. Record an integrity checksum of the encrypted result and enough non-secret metadata to map it to the correct Compose project. Check retention and secure deletion policy.
4. Restore first into **new disposable volumes**, never over the only copy of live state. Verify integrity before extraction and ownership afterward. Use isolated fixture state for initial tests; avoid exposing copied credentials to an untrusted host or third-party tool.
5. Start the matching image against the restored test volumes. Check `dev` permissions, fixture files, host-key fingerprint and safe synthetic runtime tests. An account holder then verifies legitimate account access privately, considering token expiry and provider revocation.
6. Record the result and recovery limitations. Only after a successful drill should an operator choose a live recovery/migration procedure. Keep the previous volumes intact until acceptance.

Plaintext tar/checksum recipes alone do not establish credential-safe backup. Encryption/key management, crash consistency, large-vault behavior and migration between endpoints still require dedicated acceptance work.

## Resource limits

Private `.env` controls `CONTAINER_MEMORY_LIMIT`, `CONTAINER_CPUS` and `CONTAINER_PIDS_LIMIT`; defaults are 4 GiB, 2 CPUs and 512 processes. Choose limits for the host and workload rather than assuming these are validated minimums. Render/validate the configuration and recreate the service for changes to take effect.

```sh
docker compose config -q
docker inspect "$(docker compose ps -q agent)" \
  --format 'memory={{.HostConfig.Memory}} nano_cpus={{.HostConfig.NanoCpus}} pids={{.HostConfig.PidsLimit}}'
docker stats --no-stream "$(docker compose ps -q agent)"
```

Compose configuration validation does not prove the target platform enforces every limit. These are standalone Compose runtime settings, not a claim of Swarm/Kubernetes support. Investigate out-of-memory termination and process limits before removing safeguards.

## Recovery triage

- **Session disappeared:** reconnecting does not resurrect processes after restart. Recover files/checkpoints and start a new tmux/Claude session.
- **Home or workspace appears empty:** confirm endpoint, project name and volume attachments before creating new state or deleting anything.
- **Authentication failed after recreation:** confirm the full home volume is attached; then consider expiry/revocation and client changes. Reauthenticate through supported commands instead of posting tokens or editing credential JSON.
- **Host-key warning:** verify the expected persistent key through the host console before changing client trust.
- **State truly deleted:** use a previously verified protected backup. The repository has no hidden recovery copy.

Use [diagnostics](diagnostics.md) and [troubleshooting](troubleshooting.md), and report reproducible redacted defects through [contribution guidance](../CONTRIBUTING.md).
