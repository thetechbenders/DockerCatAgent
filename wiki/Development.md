# Development

Start with the [development guide](../docs/development.md) and [contribution guide](../CONTRIBUTING.md). Select defined work from live issues and keep changes focused and reviewable.

| Topic | Source |
| --- | --- |
| Source layout and runtime files | [Source layout](../docs/development.md#source-layout) |
| Shell/Compose/static checks | [Local validation](../docs/development.md#local-static-checks) |
| Building and disposable runtime regression tests | [Build/runtime](../docs/development.md#build-and-runtime) |
| Optional trusted proxy CA build secret | [Build-network CA](../docs/development.md#optional-trusted-build-network-ca) |
| Exact-head CI and review evidence | [CI evidence](../docs/development.md#ci-evidence-and-documentation-review) |
| Manual versus synthetic acceptance | [Validation matrix](../docs/validation.md) |
| Security reporting | [Private reporting policy](../SECURITY.md) |
| Product direction and dependencies | [Roadmap](../ROADMAP.md) |
| Accepted choices and outstanding decisions | [Architecture decisions](../docs/architecture-decisions.md) |
| Wiki review/export/publish separation | [Wiki synchronization](../docs/wiki-publishing.md) |
| Issues, labels, milestones and project status | [Repository governance](../docs/github-management.md) |

CI must use harmless fixtures without personal Claude/Mem secrets. Static checks and version output cannot stand in for real OAuth, host or hardware acceptance. Inspect the run's exact head SHA and resolve failures/warnings before claiming success.

The foundation source was merged through [PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1); green CI does not establish product acceptance or authorize a release. No license has been selected, and distribution still requires an owner decision.

[Documentation home](Home.md).
