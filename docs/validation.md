# Foundation validation and acceptance

The [roadmap](../ROADMAP.md) defines milestone completion. This guide defines evidence types and reproducible checks; current outcomes belong in [foundation audit](foundation-audit.md), the exact-head CI run and canonical issues. It does not declare every listed test complete.

## Evidence matrix

| Requirement | Feasible automated evidence | Additional acceptance |
| --- | --- | --- |
| Official Claude distribution | Signed repository/key policy, actual image build and `claude --version` | Reproducibility and future upstream/key changes remain separate |
| Base non-root CLI | UID/GID, Git/tmux execution, writable home/workspace | Actual workload and host limits |
| Home/workspace persistence | Harmless fixtures across recreation/rebuild using same volumes | Real account state and provider token lifetime |
| No default exposure | Compose/inspect assertions for ports, mounts and capabilities | Target-host network policy |
| Optional SSH | Effective config, disposable-key login and negative controls | Real remote/VPN/mobile clients and host identity verification |
| Optional vault | Mount mode, fixture read and denied write, explicit write opt-in | Chosen host path, ACL/UID and actual vault/privacy review |
| Claude login | CLI command availability only | Consenting account-holder subscription/OAuth and API-key workflows |
| Mem | Supported MCP setup flags and callback transport fixture | Provider OAuth, grants, minimal real request and continuity |
| ARM64 | Static platform independence alone is insufficient | Actual ARM64 build/runtime hardware record |
| Portainer | Complete build context and image-only stack parsing | Actual endpoint/version, project and state acceptance |
| Documentation | Source cross-check, links and shell-syntax checks | Human account/client walkthroughs |

## Static and Compose checks

Run [development checks](development.md#local-static-checks), then `python3 tests/runtime_check.py` against the built local image for the disposable runtime regression suite. Validate every optional configuration you plan to enable, plus combinations such as SSH with one selected vault mode. A syntactically valid mount or port setting is not a successful runtime test.

## Basic CLI runtime

Against a disposable container with the base profile:

```sh
docker compose build --pull
docker compose up -d
docker compose exec -T -u dev agent /usr/local/bin/dockercat-smoke
docker compose exec -T -u dev agent sh -c 'test "$(id -u)" = 1000 && test "$(id -g)" = 1000'
```

Record the installed version and image ID. Inspect actual published ports, security options, capabilities and mounts without sharing a full environment dump. Confirm no default host port, host Docker socket or broad host bind. The CLI health check establishes command/directory availability, not provider connectivity or authentication.

## Harmless persistence probes

Use a disposable project and uncredentialed home. These commands refuse to overwrite existing markers:

```sh
docker compose exec -T -u dev agent sh -eu -c \
  'test ! -e /workspace/.dockercat-validation; test ! -e /home/dev/.dockercat-validation; printf workspace > /workspace/.dockercat-validation; printf home > /home/dev/.dockercat-validation'
docker compose up -d --force-recreate
docker compose exec -T -u dev agent sh -eu -c \
  'test "$(cat /workspace/.dockercat-validation)" = workspace; test "$(cat /home/dev/.dockercat-validation)" = home'
```

Rebuild and repeat the checks with the same volume attachments. Automated regressions can add dummy files at version-relevant Claude configuration paths in an isolated home; never overwrite real credentials. Verify that tmux/running commands do **not** survive recreation. Document the behavior when changing project name/endpoint: selecting different volumes is distinct from deleting data.

[Issue #15](https://github.com/thetechbenders/DockerCatAgent/issues/15) tracks the synthetic recreation requirement. Actual live account continuity belongs to authentication acceptance, regardless of that issue's completion state.

## Optional SSH regression scenarios

Use a generated disposable client key and no external account. Test effective daemon settings, a successful `dev` login and these negative paths:

- Root, password, keyboard-interactive and unauthorized-key login denied.
- Authorized-key input must be an existing nonempty regular file; no missing-path directory is implicitly created.
- Callback port must be canonical decimal 1024..65535, without leading zeroes.
- Local forwarding reaches a harmless listener only at the selected loopback callback destination; a different port/destination is denied.
- Remote, agent, X11, Unix-socket and tunnel forwarding restrictions remain effective where the scenario is exercised.
- Host-key fingerprint is unchanged through recreation with the same host-key volume.

Requesting a forbidden forward is not enough: trigger an actual connection and assert rejection. `ssh -N` can stay alive with a local listener even when a later destination connection is denied. Record which controls were tested by network behavior and which by effective configuration only.

[Issue #3](https://github.com/thetechbenders/DockerCatAgent/issues/3) tracks canonical SSH controls. A loopback fixture is not real VPN/mobile acceptance.

## Optional vault scenarios

Mount a disposable host directory using `compose.obsidian.yml`. Read a harmless marker as `dev`, inspect `RW=false`, attempt a write and assert that the host remains unchanged. Use a fresh disposable fixture for explicit write mode and confirm the intended write reaches only that directory. Confirm the base has no `/vault` mount. Test host UID/GID/ACL compatibility separately for a real vault.

[Issue #22](https://github.com/thetechbenders/DockerCatAgent/issues/22) tracks the canonical mount requirement. Synthetic success does not certify a user's actual vault, sync system or disclosure policy.

## Manual account and host gates

- [#4: Claude subscription/OAuth](https://github.com/thetechbenders/DockerCatAgent/issues/4): a consenting account holder logs in from a clean dedicated home, performs a minimal task and confirms auth continuity after recreation.
- [#19: API-key authentication](https://github.com/thetechbenders/DockerCatAgent/issues/19): validate the supported flow and credential visibility boundaries without publishing a key or weakening runtime permissions.
- [#21: live Mem/headless OAuth](https://github.com/thetechbenders/DockerCatAgent/issues/21): confirm the fixed callback, actual grant, minimal permitted request and continuity privately.
- [#2: ARM64](https://github.com/thetechbenders/DockerCatAgent/issues/2): record actual architecture, build, runtime and optional profile outcomes.
- Portainer and real remote/mobile SSH require actual endpoint/client evidence; parser and loopback tests are insufficient.

Use harmless data, explicit consent and supported login commands. Keep tokens, account identifiers, callback URLs and private provider responses out of public logs. Publish only a redacted result, scenario, code SHA and relevant versions. Report external permissions/hardware/account dependencies explicitly rather than claiming a pass.
