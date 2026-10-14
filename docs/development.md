# Developing and validating the foundation

Use the [contribution guide](../CONTRIBUTING.md), live issues and the [roadmap](../ROADMAP.md) to select a focused task. The current foundation remains in draft PR #1. Code and documentation changes belong on reviewed branches; do not push to `main`, merge or publish a wiki/image as a side effect of development.

## Source layout

| Path | Purpose |
| --- | --- |
| `Dockerfile` | Debian tooling, official Claude installation, identity and entrypoint |
| `compose*.yml` | Base, optional SSH/vault overlays and image-only Portainer stack |
| `config/sshd_config.template` | Explicit key-only SSH and restricted forwarding policy |
| `scripts/` | Startup, CLI health and smoke checks |
| `tests/` | Focused static and runtime regression checks |
| `.github/workflows/ci.yml` | Foundation static/build/runtime gate |
| `.github/` | Templates and declarative governance metadata |
| `docs/` | Canonical version-controlled operator/developer guides |
| `wiki/` | Reviewed-source navigation pages prepared for future synchronization |
| `ROADMAP.md` | Milestone scopes, dependencies and acceptance gates |

## Local static checks

From the complete checkout:

```sh
for script in scripts/*.sh .github/*.sh; do bash -n "$script"; done
python3 tests/static_check.py
docker compose -f compose.yml config -q
SSH_AUTHORIZED_KEYS_FILE="$PWD/.env.example" \
  docker compose -f compose.yml -f compose.ssh.yml config -q
OBSIDIAN_VAULT_PATH="$PWD/wiki" \
  docker compose -f compose.yml -f compose.obsidian.yml config -q
OBSIDIAN_VAULT_PATH="$PWD/wiki" \
  docker compose -f compose.yml -f compose.obsidian-write.yml config -q
docker compose -f compose.portainer.yml config -q
```

The `.env.example` key-file value is a **parser fixture**, not an authorized-key file for an actual SSH service. These checks must not start SSH with that file. A real SSH fixture uses a generated disposable key and a preexisting protected public-key file.

Static assertions cover selected unsafe defaults, installation policy, mounts and source hygiene. They cannot establish actual authentication, effective SSH behavior, write denial or persistence. Treat warnings and failed checks as defects to investigate.

## Build and runtime

Use Docker Engine when available, without real Claude/Mem credentials or personal vault files. Start with the [validation guide](validation.md); the image's smoke entrypoint is:

```sh
docker compose build --pull
docker compose up -d
docker compose exec -T -u dev agent /usr/local/bin/dockercat-smoke
```

Run `python3 tests/runtime_check.py` after building `dockercatagent:local` to exercise the disposable runtime regression suite. It creates unique temporary Compose projects and synthetic key/vault/state fixtures without real accounts. Use a disposable Compose project for any additional fixtures so a test cannot overwrite an operator's home or workspace. Verify base exposure, mounted volume continuity and optional-profile runtime behavior. The [CI workflow](../.github/workflows/ci.yml) is the authority for current automated commands; [audit evidence](foundation-audit.md) records their disposition.

Do not inject personal credentials into CI. A synthetic `.claude` fixture tests volume placement, not a live token. Account-holder acceptance remains in the relevant issue.

## Optional trusted build-network CA

Some build networks use a trusted HTTPS proxy. If necessary, supply the operator-approved CA **bundle** as a BuildKit secret; keep TLS verification enabled:

```sh
docker build --build-arg HTTP_PROXY --build-arg HTTPS_PROXY --build-arg NO_PROXY \
  --secret id=proxy_ca,src=/path/to/trusted-ca-bundle.pem \
  -t dockercatagent:local .
```

The build arguments use the caller's already configured proxy variables. The path is an operator-supplied local bundle, not committed sample data. The optional secret is mounted for the network build steps and is not installed in the image or persisted into runtime state. Do not copy private proxy credentials or certificates into source, disable certificate checking or broaden runtime trust merely to make a build pass. Ordinary hosts use the normal build command without the secret.

## CI evidence and documentation review

`Foundation CI` runs on pull requests and manual dispatch. Inspect the run's head SHA before using it as evidence: a successful older branch run does not validate new changes. Read failed steps through completion, fix in scope and verify the resulting exact-head run. Use existing successful evidence when no meaningful code/test changes justify another build.

A useful PR states the defect/outcome, security boundaries changed, relevant commands and actual results, and pending manual gates. Check local documentation links and shell snippets; replace hypothetical working integrations with explicit unvalidated procedures. Keep wiki publishing separate, using the [reviewed synchronization guide](wiki-publishing.md).
