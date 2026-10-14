# DockerCatAgent roadmap

This roadmap describes capability outcomes for the four GitHub milestones: **Foundation**, **Access & Reliability**, **Developer Experience**, and **Exploration**. It makes no release-date or version commitment. Open issues carry detailed acceptance criteria; milestone completion must follow evidence rather than a green badge alone.

## Current reality

The foundation is implemented on `feat/claude-docker-foundation` and remains under review in [draft PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1). Its presence on that branch is separate from acceptance or availability on `main`.

| Workstream | Present on the review branch | Evidence still required |
| --- | --- | --- |
| Container | Debian image, upstream Claude Code installation, Git/tmux/tooling, non-root default, resource limits, CLI health check | Clean build and runtime evidence for the exact reviewed commit; ARM64 host acceptance [#2](https://github.com/thetechbenders/DockerCatAgent/issues/2) |
| State | Named volumes for the workspace and complete user home | Recreation/rebuild tests [#15](https://github.com/thetechbenders/DockerCatAgent/issues/15); real authenticated-state retention [#4](https://github.com/thetechbenders/DockerCatAgent/issues/4), [#19](https://github.com/thetechbenders/DockerCatAgent/issues/19), [#21](https://github.com/thetechbenders/DockerCatAgent/issues/21) |
| SSH | Optional overlay, key-only `dev` login, restricted local forwarding, persistent host-key volume | Effective configuration and connection/denial tests [#3](https://github.com/thetechbenders/DockerCatAgent/issues/3); operator-specific remote client and network validation |
| Integrations | Optional Obsidian overlays and user-local Mem setup guide | Mount/default/write-opt-in tests [#22](https://github.com/thetechbenders/DockerCatAgent/issues/22); consenting-account Mem OAuth [#21](https://github.com/thetechbenders/DockerCatAgent/issues/21) |
| Deployment and docs | Compose build context, image-only Portainer configuration, repository guides and wiki source | Actual Portainer endpoint test [#5](https://github.com/thetechbenders/DockerCatAgent/issues/5); reviewed wiki publication [#14](https://github.com/thetechbenders/DockerCatAgent/issues/14) |
| Distribution | Source under review; no approved release or registry image | Owner license and notice decision [#6](https://github.com/thetechbenders/DockerCatAgent/issues/6), review approval, and an explicit later release decision |

The [audit report](docs/foundation-audit.md) and [validation guide](docs/validation.md) describe check results and their limits. This table names evidence obligations; a linked validation issue may close when that specific evidence is recorded without implying that every foundation gate has passed.

## Foundation

**Outcome:** an initial usable Claude Code container with persistent files and account state, a secure default runtime, and documented optional access paths.

The implementation scope is the existing Dockerfile and Compose configurations, official Claude distribution, non-root interactive use, Git and tmux, named workspace/home volumes, configurable resource limits, shell scripts, and credential-free CI. SSH, Obsidian, and Mem remain opt-in. Portainer uses a complete build context or a locally built image on the same Docker endpoint.

Validation work is distinct from implementation work:

- **Automated/static:** shell syntax, effective Compose configuration, static security and path checks, default lack of published ports, documentation command consistency, and repository secret hygiene.
- **Synthetic runtime:** build and installed versions, actual non-root writes, container recreation/rebuild without lost files, SSH effective configuration and allowed/denied connection cases, host-key retention, and optional Obsidian mount behavior. Tests use disposable keys, files, and volumes.
- **Manual/account-backed:** subscription OAuth [#4](https://github.com/thetechbenders/DockerCatAgent/issues/4), optional API-key behavior [#19](https://github.com/thetechbenders/DockerCatAgent/issues/19), and Mem headless OAuth [#21](https://github.com/thetechbenders/DockerCatAgent/issues/21). These require consenting account holders; credentials must never enter CI or public reports.
- **Manual/host-specific:** ARM64 hardware [#2](https://github.com/thetechbenders/DockerCatAgent/issues/2), real Portainer build-context deployment [#5](https://github.com/thetechbenders/DockerCatAgent/issues/5), and the operator's SSH/VPN client path. An AMD64 CI runner cannot establish those outcomes.

### Foundation acceptance gate

Foundation is complete only when:

1. The exact reviewed commit builds cleanly and its relevant static and runtime checks pass with no unresolved security or installation defect.
2. Claude, Git, and tmux execute; `dev` can write the workspace and home without root in the default runtime; no ports or broad host access appear by default.
3. Workspace, Claude home/configuration, and SSH host identity survive supported recreation/rebuild paths. Process lifetime is accurately documented: tmux and running commands end when a container ends.
4. Optional SSH enforces public-key-only non-root login and restricted forwarding, and optional Obsidian read-only mounting actually rejects writes. Write access stays an explicit opt-in.
5. Real subscription, optional API-key, and optional Mem authentication/state-lifecycle acceptance is recorded by consenting account holders. These named validation obligations remain pending until tested, even when users can omit the optional integrations.
6. ARM64 hardware and an actual Portainer endpoint have acceptance evidence; supported architecture/deployment claims match those results. Until then, documentation limits support claims and the corresponding Foundation obligations remain open.
7. Installation, security, maintenance, and contributor documentation match the tested implementation, and remaining manual obligations are visible in canonical issues.

Passing this gate does not authorize a merge, release, registry push, or production deployment. The license decision [#6](https://github.com/thetechbenders/DockerCatAgent/issues/6) must precede approved redistribution; an explicit owner release decision is still required.

## Access & Reliability

**Outcome:** operators can recover state, understand the optional SSH privilege model, and assess the provenance and compatibility of updates.

| Work | Expected result | Existing tracking |
| --- | --- | --- |
| Credential-safe backup and restoration | Encrypted backup instructions, protected-key handling, full restore drill covering workspace/home/SSH identity, and documented retention and deletion | [#7](https://github.com/thetechbenders/DockerCatAgent/issues/7) |
| Migration and recovery | A state inventory, safe upgrade/rollback assumptions, configuration migration boundaries, and recovery from missing volumes or changed Compose project names | [#7](https://github.com/thetechbenders/DockerCatAgent/issues/7) |
| Dependency reproducibility and provenance | Evaluate package/version and base-image pinning, record installed versions/digests, generate useful SBOM/provenance, and define vulnerability triage and CI supply-chain checks | [#8](https://github.com/thetechbenders/DockerCatAgent/issues/8) |
| Optional SSH hardening | Review why sshd runs as root, bound its capabilities, evaluate least-privilege alternatives, and preserve proven authentication/forwarding restrictions | [#9](https://github.com/thetechbenders/DockerCatAgent/issues/9) |
| Deployment compatibility | Carry foundation hardware and Portainer evidence into explicit support limits; evaluate additional environments only with real test capacity | [#2](https://github.com/thetechbenders/DockerCatAgent/issues/2), [#5](https://github.com/thetechbenders/DockerCatAgent/issues/5) remain foundation validation |

Backup work depends on the foundation state inventory and persistence behavior, not on a release. SSH privilege changes depend on the baseline SSH regression tests. Provenance work depends on the selected upstream distribution and builds; it must distinguish documented version recording from reproducible artifacts. No next-stage item is a reason to delay a scoped foundation defect fix.

**Completion definition:** documented encrypted backup/restore and configuration migration/recovery drills succeed without exposing credentials; the SSH privilege review has an actionable disposition; dependency/provenance evidence and supply-chain update/vulnerability procedures are defined for the supported build path. Continued manual host validation remains explicit.

## Developer Experience

**Outcome:** operators and contributors can configure, diagnose, and maintain the environment with clear documentation and optional tooling.

| Work | Expected result | Existing tracking |
| --- | --- | --- |
| Environment diagnostics | A read-only preflight that reports versions, permissions, volumes, limits, and relevant network/configuration failures while redacting secrets and private paths | [#10](https://github.com/thetechbenders/DockerCatAgent/issues/10) |
| Optional development profiles | Evaluate scoped language/toolchain recipes and their maintenance cost; keep heavy toolchains optional rather than adding every candidate to the base image | [#11](https://github.com/thetechbenders/DockerCatAgent/issues/11) |
| Remote knowledge integrations | Supported user-local MCP recipes, provider permissions/account scope warnings, and headless authentication limits, without bundled private data or automatic ingestion | [#12](https://github.com/thetechbenders/DockerCatAgent/issues/12); Mem baseline validation remains [#21](https://github.com/thetechbenders/DockerCatAgent/issues/21) |
| Documentation maturity | Reviewed wiki navigation backed by canonical repository guides, a publication procedure, and a maintenance checklist | [#14](https://github.com/thetechbenders/DockerCatAgent/issues/14) |
| Mobile remote terminals | Phone/tablet SSH and tmux recipes, disconnect/reconnect and read-only observation checks, and clear distinction between a viewing convenience and access control | [#16](https://github.com/thetechbenders/DockerCatAgent/issues/16) |

Diagnostics must use the accepted state/security model and avoid collecting prompts, private vault content, or credentials. Remote-client recipes build on SSH acceptance. MCP recipes need provider-supported commands and account-holder testing for any claimed authenticated workflow. Wiki publication depends on review of its source; prepared files alone do not count as publication.

**Completion definition:** representative operators can follow the guides and use the accepted diagnostics and optional recipes, with test evidence for each supported workflow and an identified documentation maintenance path.

## Exploration

**Outcome:** owners can make informed architecture and product decisions before committing to new capabilities.

- Evaluate additional coding agents [#18](https://github.com/thetechbenders/DockerCatAgent/issues/18), including upstream distribution, credential storage, licensing, and compatibility with the single-container boundary.
- Assess remote IDE/devcontainer compatibility as a separate optional path, including extension installation, permissions, state lifecycle, and resource costs.
- Evaluate generic future MCP providers only when a concrete use case and supported authorization model exist; defined recipe work belongs in [#12](https://github.com/thetechbenders/DockerCatAgent/issues/12).
- Consider image distribution only after licensing, release scope, update/provenance policy, and publication authorization are settled. No registry publication is scheduled.

These are evaluation candidates, not shipped features or implementation instructions. New issues should follow a concrete outcome, testable criteria, scope, and owner decision; an exploratory list alone is insufficient.

**Completion definition:** each pursued candidate has a documented accept/defer/reject decision with security and maintenance tradeoffs. This milestone does not need every possible enhancement to become a feature.

## Dependencies and release readiness

The main workstreams follow this order:

1. Verify the current foundation implementation and correct confirmed defects.
2. Record synthetic/runtime acceptance, then complete account-holder and host-specific validation for the supported claims.
3. Use that state/security inventory for recovery, reproducibility, diagnostics, and client recipes.
4. Review source and documentation; obtain an owner license/notice decision before redistribution.
5. Decide separately whether and how to release. Releases, public images, tags, and deployments require explicit authorization.

The license decision is an owner dependency for redistribution; it does not prevent credential-free local checks. Mem and Obsidian are optional and do not block users who omit them. Future toolchain profiles, IDEs, and alternate agents do not block foundation acceptance. Release readiness includes licensing, documented support limits, unresolved vulnerability review, provenance/update policy, and a specific release decision; it is not inferred from milestone progress.

## Explicitly out of scope

This work does not build multi-agent orchestration, Kubernetes or Swarm infrastructure, a custom dashboard, hosted cloud services or account provisioning, public SSH exposure, privileged host controls, automatic deployment, or automatic prompt/source/knowledge ingestion. There are no bundled private personas, account credentials, personal instructions, or external knowledge-provider requirements.

Optional personal `CLAUDE.md` instructions are user-owned configuration, not an authorization boundary. Read-only Obsidian mounts prevent filesystem writes but do not authorize disclosure, and prompts/tool filters do not revoke upstream MCP account scopes.

## Project decisions

- Claude Code first; Compose is the authoritative runtime configuration.
- SSH, Obsidian, and Mem are optional. SSH host publication defaults to loopback.
- The user home and workspace persist; running processes do not survive container recreation.
- Repository source and wiki preparation remain reviewable through pull requests.
- The owners have not selected a software license. No release, registry image, merge, or deployment is authorized by this roadmap.
