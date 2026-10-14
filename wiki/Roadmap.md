# Roadmap and Development Status

The [repository roadmap](../ROADMAP.md) is the canonical milestone/dependency description. GitHub [issues](https://github.com/thetechbenders/DockerCatAgent/issues) and [milestones](https://github.com/thetechbenders/DockerCatAgent/milestones) track actionable outcomes; none is a release promise or version number.

| Milestone | Outcome |
| --- | --- |
| Foundation | Usable container, persistent state, baseline security and explicit foundation acceptance |
| Access & Reliability | SSH hardening, recovery, supply-chain reproducibility, backup/restore and compatibility |
| Developer Experience | Operator tools, mature documentation, optional profiles/integrations and remote-terminal usability |
| Exploration | Ideas requiring an explicit product/architecture decision |

The [validation guide](../docs/validation.md) separates implementation from testing and release readiness. Green synthetic CI does not complete manual account, architecture or deployment gates. Foundation remains incomplete while required acceptance is outstanding.

Candidates such as diagnostics, profile tooling, migration, IDE compatibility and other coding agents do not authorize immediate implementation. Multi-agent orchestration, Kubernetes, custom dashboards and hosted infrastructure remain out of scope. Releases, registry images and production deployments require separate approval. Licensing is an owner decision.

See [governance](../docs/github-management.md), [audit evidence](../docs/foundation-audit.md) and [Development](Development.md). [Documentation home](Home.md).
