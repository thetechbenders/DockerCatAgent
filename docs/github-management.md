# GitHub project management

GitHub Issues track outcomes, [ROADMAP.md](../ROADMAP.md) sets scope and sequencing, and [wiki/](../wiki/Home.md) contains reviewed-source wiki drafts. Milestones are capability goals, with no invented versions or due dates. Issue counts are not a measure of engineering progress.

## Applied taxonomy

On 2026-10-14, authenticated GitHub CLI/API calls created and read back the 19 missing labels from [labels.json](../.github/labels.json). The nine pre-existing labels were preserved, including their conventional-label descriptions. Every open issue has one primary type, one or two relevant areas, one priority and at most one current workflow status. Duplicate issues also use the existing `duplicate` label.

| Family | Meaning and color convention |
| --- | --- |
| `type:*` | Work class: bug, enhancement, documentation, security or testing; distinct colors |
| `area:*` | Container, remote access, integrations, docs or developer experience; subsystem colors |
| `priority: P0` / `P1` / `P2` / `P3` | Red / orange-red / amber / muted green |
| `status: blocked` | Red; name the actual dependency or decision |
| `status: needs-validation` | Pale yellow; behavior exists but acceptance evidence is incomplete |
| `status: ready` | Green; scoped work can begin |
| `status: needs-triage` | Neutral gray; requires scope or architectural decisions |

Do not apply `good first issue`, `help wanted` or `breaking change` merely for visual variety. Labels organize work; color alone is not a security-severity guarantee.

## Live milestones

The four live milestones match [milestones.json](../.github/milestones.json) and the roadmap. Their descriptions define outcomes and completion criteria:

- **Foundation:** initial usable Docker/Compose CLI, persistent state, baseline security and foundation acceptance. Green CI alone cannot complete account, hardware or deployment validation.
- **Access & Reliability:** SSH least privilege, credential-safe backup/restore, configuration recovery/migration and reproducible supply-chain maintenance.
- **Developer Experience:** private diagnostics, optional tooling/integration recipes, documentation maintenance and remote-terminal usability.
- **Exploration:** assessments and explicit go/no-go decisions; no implementation commitment.

The maintainer bootstrap is a reversible, non-deleting metadata reconciliation tool. Inspect its preview before applying it:

```bash
.github/bootstrap-github.sh
APPLY=1 .github/bootstrap-github.sh
```

It upserts manifest labels and milestone descriptions and verifies their live values. It preserves unrelated labels, existing milestone states and due dates. Assigning issues is a separate evidence-based triage task. Do not reopen completed work when resynchronizing the taxonomy.

## Canonical issues and evidence

The circular duplicate closures were reconciled: [#3](https://github.com/thetechbenders/DockerCatAgent/issues/3) is canonical for SSH validation and #17 is its closed duplicate; [#6](https://github.com/thetechbenders/DockerCatAgent/issues/6) is canonical for licensing/contribution/notice decisions and #13 is its closed duplicate. Both canonical requirements were unresolved when reopened.

[#4](https://github.com/thetechbenders/DockerCatAgent/issues/4) tracks subscription authentication; #19 tracks API-key authentication and exposure boundaries; #21 tracks optional Mem OAuth. Harmless persistence fixtures in #15 do not prove real authentication continuity. ARM64 hardware (#2), Portainer endpoint acceptance (#5) and other manual validations retain explicit acceptance criteria.

Give each issue a concrete outcome, testable criteria, constraints and meaningful dependencies. Consolidate criteria into one canonical issue and close duplicates with a one-way reference. Close validation tasks only when their evidence supports every criterion; otherwise record completed portions and remaining work. Keep implementation, synthetic validation, manual account/host acceptance and release decisions distinct.

## Project and repository administration limitations

**Project #2 is the owner-designated canonical DockerCatAgent planning board.** Use that project; do not create another. Its organization URL is expected to be https://github.com/orgs/thetechbenders/projects/2; the exact URL/owner is awaiting confirmation. Reading organization Project #2 and the repository-linked project currently fails with `Resource not accessible by integration`. This prevents inspecting fields/items or safely changing the board through the available identity. No board changes are claimed.

Earlier listings exposed no accessible equivalent project, and an attempted creation was denied with `Resource not accessible by integration (createProjectV2)`; no duplicate board was created. Issues, labels and milestones remain organized while board access is unavailable.

When the canonical project's write access is available, inspect its existing organization before editing it. Reuse native issue state and milestones alongside existing project Status values. Preferred views are Backlog, Ready / In Progress / Blocked, Milestones, Foundation validation, and Future enhancements. Add canonical repository issues, preserve unrelated project items/fields, and read back every change. These are a configuration handoff, not a claim that views were created.

Repository description/topics editing and branch-protection inspection were also denied by the integration. The observed description remains `Docker Agent Cli` and no topics were applied. Suggested owner-set description: “A Docker/Compose foundation for persistent Claude Code CLI work, with optional SSH and integrations. Under development.” Suggested topics: `docker`, `docker-compose`, `claude-code`, `cli`, `tmux`. The branches endpoint reported main with `protected: false`; detailed branch-protection configuration could not be inspected through this integration.

## Pull requests and wiki publishing

Use feature branches and draft PRs. Never push directly to main, force-push or merge without explicit authorization. Validate the exact current head and inspect warnings/failures. The [foundation audit](foundation-audit.md) records what synthetic checks establish and what remains manual. No license, release, image publication or production deployment is implied by CI.

Wiki is enabled, but source pages are **prepared only**. The [publishing procedure](wiki-publishing.md) describes how an approved source commit can later be synchronized to the separate wiki Git repository without competing documentation authorities. Do not publish an unreviewed wiki independently of its PR.
