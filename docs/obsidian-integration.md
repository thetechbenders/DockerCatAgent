# Optional Obsidian vault mount

A vault is a host directory of Markdown and attachments. DockerCatAgent does not run the Obsidian desktop application, require an Obsidian API plugin or index notes automatically. The base service mounts no vault.

## Read-only access

Set `OBSIDIAN_VAULT_PATH` in private `.env` to an existing directory on the **Docker endpoint host**. A path on your laptop is not available to a remote Docker daemon merely because the CLI runs there.

```dotenv
OBSIDIAN_VAULT_PATH=/absolute/path/to/existing/vault
```

From the checkout on the Docker host:

```sh
docker compose -f compose.yml -f compose.obsidian.yml config -q
docker compose -f compose.yml -f compose.obsidian.yml up -d
docker compose -f compose.yml -f compose.obsidian.yml exec -u dev agent bash
```

The selected directory appears at `/vault` with `read_only: true`. Confirm UID/GID 1000 can traverse and read only the intended host path. Do not use recursive `chmod 777`, mount an entire host home, or make the container privileged to fix a permission problem.

Verify the Docker mount's read-only property and an actual denied write with a **disposable test vault**, as described in [validation](validation.md). Configuration parsing alone does not establish a host mount works. [Issue #22](https://github.com/thetechbenders/DockerCatAgent/issues/22) tracks host vault acceptance.

## Write access is a separate opt-in

Use `compose.obsidian-write.yml` instead of `compose.obsidian.yml` only after explicitly accepting write access. Do not combine them. Keep a protected backup and test against a disposable vault before granting an agent a real writable vault. Writes, deletions, concurrent Obsidian sync and generated filenames can affect the host's data; this project provides no conflict resolver, snapshot or rollback service.

## Privacy and task boundaries

Read-only prevents filesystem modification, not data disclosure. Files, attachments, plugin settings and metadata may contain secrets. Mount the smallest useful directory and review what a prompt can send to Claude or other tools.

A generic task can be: “Read Markdown in `/vault/Projects/Example`, summarize the decisions with file citations, and do not modify files.” This is task guidance, not an enforced disclosure policy. Inspect repository and vault instructions as untrusted content. See [security](security.md) and [integration permission boundaries](integrations.md).
