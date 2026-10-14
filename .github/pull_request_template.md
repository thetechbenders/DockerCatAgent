## Problem and result
Describe the concrete problem, the resulting behavior, and the smallest reviewable change.

## Issue and scope
Link the canonical issue. Identify implementation, validation, documentation, or owner-decision work and any relevant dependencies. Use closing keywords only when this PR satisfies the issue's acceptance criteria.

## Verification
Record commands, results, and the tested commit. Distinguish static checks, synthetic runtime checks, and account-holder/host-specific manual tests. Mark inapplicable checks and explain unavailable ones.

- [ ] Relevant shell/static checks pass
- [ ] Resolved Compose configurations for affected overlays pass
- [ ] Relevant Docker build and runtime regressions pass
- [ ] Secret/path hygiene and security implications reviewed
- [ ] Documentation and support claims match evidence
- [ ] Required manual acceptance recorded or explicitly deferred

## Security and data handling
What network, filesystem, credential, and authorization surfaces changed?

## Deferred work
List remaining manual validation, known limitations, and follow-up issues. Do not include tokens, private keys, personal account data, or OAuth callback URLs. Green CI alone does not authorize a merge or release.
