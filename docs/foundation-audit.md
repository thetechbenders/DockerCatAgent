# Foundation audit and evidence

> **Historical audit:** This document records the original foundation validation, before the independent review. Its early SSH capability changes and noninteractive-login evidence were superseded by the remediation in draft [PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1). Check that PR's latest verified exact-head CI for the current capability set and real PTY/tmux tests. The local image identifier, source head and test counts below describe the earlier audit only.

This audit covers draft [PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1), not a merged release or deployment. The starting main commit was `a8cef525bb7e74aa304a1033fc53912bd82553ab`; the live foundation branch had advanced to `e46cb784b6ebbe2576318e93608652e4c8a5cf75` before this work. Existing [CI run 38567218508](https://github.com/thetechbenders/DockerCatAgent/actions/runs/38567218508) passed for that associated head. Logs show checkout of PR merge ref `ceb31d1784c0846b39cd3b1a958ef4d66c8aa9d7`; its Git tree was verified identical to the foundation head. The updated workflow explicitly checks out the branch head. Existing logs were inspected before rebuilding.

## Verified defects and scoped corrections

| Finding | Correction and regression |
| --- | --- |
| Debian package installation generated default SSH private host keys in the image | Remove package-generated host keys in the install layer; assert they are absent and use only the persistent runtime identity |
| Optional SSH initially failed because the root entrypoint chmod required `FOWNER` | **Historical correction only:** `FOWNER` was temporarily granted. Later independent review eliminated the root chmod of the dev-controlled path and removed `FOWNER`; PTY regression coverage now tests actual interactive login. |
| OpenSSH then failed its pre-authentication chroot without `SYS_CHROOT` | Add `SYS_CHROOT` only to SSH; exercise login and denial/forwarding behavior |
| Callback input accepted leading-zero arithmetic that Bash interprets as octal | Require bounded canonical decimal input and reject malformed/out-of-range values |
| A directory could satisfy the former nonempty-key check; Compose could create a directory for a missing bind source | Require a nonempty regular key file and disable bind-source creation for explicit SSH/vault paths |
| `bash -n scripts/*.sh` parsed only the first script | Iterate over every runtime and management shell script in CI and contributor commands |
| Documented bootstrap invocation failed because its file was not executable | Set executable mode and verify dry-run plus authenticated apply/read-back |
| Bootstrap only created missing milestones and did not reconcile or verify descriptions | Upsert manifest descriptions without changing milestone state/dates; verify live labels and milestone values |
| Existing checkout action emitted a Node 20 deprecation warning | Pin the inspected current Node 24 checkout action commit, disable persisted checkout credentials and explicitly check out the PR head |
| Managed proxy TLS trust was absent during the local image build | Add optional transient BuildKit CA-bundle support, preserve TLS verification, and confirm it is absent from runtime |
| Debian slim excluded installed package manpages, producing broken alternative-link warnings | Retain package manpages before installation; keep other slim exclusions and installed tools |

**Current SSH capability roster differs from this historical audit:** `AUDIT_WRITE`, `SETUID`, `SETGID`, `CHOWN`, `SYS_CHROOT`, `DAC_READ_SEARCH` in the opt-in overlay. The independent review also corrected first-boot public host-key recovery and documented ownership requirements; see the PR's latest exact-head CI.

No default capabilities, ports, host namespaces, Docker socket, registry publication or account provisioning were added. SSH remains a root daemon with non-root sessions; its expanded explicit capability set is a residual risk for [#9](https://github.com/thetechbenders/DockerCatAgent/issues/9), not a claim of rootless operation.

## Implementation review

- Claude comes from the official signed Debian distribution. The build checks the upstream signing-key fingerprint, uses `signed-by`, keeps TLS verification enabled and runs `claude --version`. Mutable channels/base tags still prevent a reproducible-build guarantee; [#8](https://github.com/thetechbenders/DockerCatAgent/issues/8) tracks policy/provenance.
- Both image and base Compose select UID/GID 1000. Workspace and complete home are dedicated named volumes, preserving `.claude.json`, `.claude/` and version-dependent user-local state without guessing one credential filename.
- Default Compose publishes no ports, drops all capabilities, enables `no-new-privileges`, and has configurable CPU/memory/PID limits. It mounts no host directory or Docker socket. Outbound access is available; no egress policy is implemented.
- Optional SSH disallows root/password/keyboard-interactive login and uses an authorized-key file, persistent Ed25519 identity and local-only callback destination restrictions. Effective configuration and actual connection tests must be reported separately.
- Obsidian is absent by default. Read-only and write overlays are separate explicit choices. A read-only mount does not prevent disclosure of readable data to an authorized external provider.
- Mem is optional user-local MCP configuration. CLI command availability can be tested without an account; provider OAuth and grants cannot.
- The health check tests CLI prerequisites and directories. There is no invented HTTP service or authenticated-provider health claim.
- Portainer uses a prebuilt image on the chosen endpoint from the complete source context. Parser/local image tests cannot prove a real Portainer deployment.
- Repository files, ignore/build-context rules, docs and templates were checked for credential patterns and accidental private/runtime personalization. Pattern checks are limited detection, not a forensic guarantee.

## Validation disposition

The results and local image ID below are from the **pre-review** implementation, not the current PR head. Real interactive PTY/tmux testing, signing-key-negative cases, and current regression outcomes are tracked in the PR verification section.

Local checks passed on 2026-10-14 using AMD64 Docker 28.4.0 and Compose v2.40.3. The built image was `sha256:6a30b29c00db4de9a635aff38549f86201ca8e761339dfa89e6ddac35063a5fb`, with Claude Code `2.1.287`, Git `2.39.5` and tmux `3.3a`. The final build emitted no warning/error markers. This is a local image identifier, not a published registry digest.

| Executed checks | Result and limit |
| --- | --- |
| Per-script `bash -n`, `python3 tests/static_check.py`, YAML/JSON parsing and `git diff --check` | Passed; static checks cannot establish provider or host acceptance |
| `docker compose ... config -q` for base, SSH, each vault, SSH with each vault and Portainer | Passed; real Portainer endpoint remains untested |
| Docker BuildKit image build with inherited proxy/TLS and transient CA secret | Passed; no CA secret, proxy environment or package-generated host identity embedded in the runtime image |
| `python3 -u tests/runtime_check.py` | Passed: UID/GID, Claude/Git/tmux, workspace/home writes, no default ports/vault/socket, home/workspace fixtures, process loss and CLI health prerequisites |
| Separate same-project rebuild/recreation drill and differently named project | Passed: cached rebuild retained the same image ID; fixtures and permissions survived, tmux ended, new project selected fresh independent volumes. This was not an image-version upgrade or migration drill |
| Synthetic vault read-only/write overlays | Passed: read works, read-only filesystem rejects mutation, explicit write works under dev. Host ACL/filesystem behavior remains operator-specific |
| Disposable-key SSH client, effective daemon configuration and callback listener | Passed: dev login; missing/wrong-key, root/password, prohibited destination, remote forward and agent forward denial; loopback host binding and host identity persistence. Tunnel/Unix-socket restrictions are effective-config evidence, not an actual tunnel-device test |
| Credential/path hygiene, documentation commands and links | Passed: 234 local Markdown links/anchors and 34 shell documentation blocks; official Claude distribution and available MCP flags cross-checked. No live account secrets were used |
| Bootstrap preview plus authenticated apply/read-back | Passed: actual label colors/descriptions and milestone definitions verified, with unrelated metadata preserved |
| Temporary wiki export | Passed: 11 prepared pages rewritten to approved-format source links; no wiki remote writes |

Disposable containers, fixture keys and test volumes were cleaned up. The final published code SHA and exact-head CI result are recorded in [PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1); the workflow runs static and credential-free runtime jobs. The [validation guide](validation.md) defines reproducible checks and evidence boundaries.

## Remaining acceptance and security limitations

- Subscription login/state continuity (#4), API-key exposure/billing behavior (#19), and Mem headless OAuth/grants (#21) require consenting account holders and are not automated.
- ARM64 hardware (#2), an actual Portainer endpoint (#5), and real VPN/mobile remote clients remain untested here. Actual tunnel-device denial remains outstanding in #3; its configured restriction was verified.
- Encrypted backup/restore and configuration migration drills (#7), root SSH least-privilege review (#9), and reproducibility/provenance (#8) belong to later scoped work and were not implemented.
- Docker administrators can access secret-bearing state; ordinary outbound access is enabled. Read-only vaults and prompt/tool restrictions do not prevent disclosure or revoke upstream account grants.
- No license has been approved (#6). No merge, release, tag, public image, wiki synchronization or production deployment occurred.
