# GitHub project management

The repository uses GitHub Issues for deliverables, `ROADMAP.md` for strategic sequencing, and `wiki/` for **reviewable wiki source pages**. No release cadence or version numbers have been authorized.

## Proposed milestones

- **Foundation:** the Docker image, Compose, authentication/SSH/optional integration acceptance and validated documentation.
- **Access & Reliability:** state backup/restore, security regression cases and compatibility.
- **Developer Experience:** diagnostics, toolchain recipes, clients and wiki.
- **Exploration:** intentionally uncommitted ideas; not authorization to implement.

## Label taxonomy

The color-coded palette is defined in [labels.json](../.github/labels.json). Use at most one **priority** and one **status**, plus an applicable **type** and **area**. Red denotes blockers/security, orange high priority, yellow planning, purple subsystem or onboarding, green ready/integration, and blue testing/documentation. Color is a navigation aid, not a technical severity guarantee.

This connected GitHub integration does not expose native label or milestone creation. Committing a JSON manifest **does not create live labels**. A maintainer with an authenticated `gh` CLI can run:

```bash
# Preview
.github/bootstrap-github.sh

# Apply after inspecting the manifest and verifying repository permissions
APPLY=1 .github/bootstrap-github.sh
```

This script does not remove labels or milestones; it upserts labels and adds only missing milestone titles. Issue label/milestone assignment is a separate triage pass.

## Issue hygiene

Give each issue a concrete outcome, testable acceptance criteria, risk/boundary description, target stage, and optionally dependency links. Defer rather than mark complete when real Docker/SSH/OAuth validation has not occurred. Never use the backlog as evidence of released capability.

Close duplicate issues with a link to the canonical ticket. Do not use GitHub issue counts as a proxy for engineering progress.

## Pull requests

Work on feature branches, open draft PRs, validate the exact head, and provide separate evidence for static checks, container builds, real host behavior and provider logins. Green CI is not merge permission.

## Wiki publishing

The wiki pages in [wiki/](../wiki/Home.md) are authored in Git for review. Publishing or synchronizing GitHub Wiki is a distinct action after owner approval; the wiki content is not automatically live just because the folder exists.
