# Contributing

DockerCatAgent's foundation is under review in [draft PR #1](https://github.com/thetechbenders/DockerCatAgent/pull/1). Read the [roadmap](ROADMAP.md), [development guide](docs/development.md), and [existing issues](https://github.com/thetechbenders/DockerCatAgent/issues) before starting. An implemented review-branch feature may still lack account-holder or hardware acceptance.

No software license or contributor licensing policy has been approved. See [#6](https://github.com/thetechbenders/DockerCatAgent/issues/6); do not assume redistribution rights or add third-party code without resolving its licensing requirements.

## Propose or report work

Search open and closed issues before creating a ticket. Link a canonical issue when work overlaps; duplicate references should point in one direction. A useful defect report includes the source commit, sanitized Docker/Compose and Claude versions, CPU architecture, enabled overlays, reproduction commands, and expected versus observed behavior.

An enhancement needs an outcome, testable acceptance criteria, constraints, and relevant dependencies. Explain security and maintenance costs and why a proposed tool belongs in the base image or an optional profile. Candidate integrations need supported provider commands and a clear account/permission model. The exploratory roadmap does not imply an implementation commitment.

Keep tokens, private keys, private vault content, personal paths, and OAuth callback URLs out of issues and logs. Use the [security reporting policy](SECURITY.md) for vulnerabilities.

## Make a focused change

1. Refresh the repository and inspect the branch, working tree, relevant issues, and active pull requests. Preserve other contributors' work and avoid overlapping implementations.
2. Create a focused branch from the appropriate current base. Never push directly to `main`, force-push shared work, or reset another contributor's changes.
3. Keep code, documentation, and issue scope aligned. Fix verified defects with focused regressions; avoid unrelated refactoring or speculative features.
4. Run checks appropriate to the change and record exact commands, results, and the tested commit. Treat failures and meaningful warnings as defects.
5. Open a reviewable pull request, initially draft when validation is incomplete. Include the problem, resulting behavior, evidence, security implications, and explicit remaining checks.

Use your established Git identity. Keep commit messages factual; do not append promotional text, generated-session links, or attribution footers. A passing check does not authorize merging or releasing.

## Verify changes

Run the lightweight baseline checks from the repository root:

```sh
for script in scripts/*.sh .github/*.sh; do bash -n "$script"; done
python3 tests/static_check.py
docker compose -f compose.yml config -q
```

For image or runtime changes, build the complete context and exercise the non-root CLI:

```sh
docker compose build --pull
docker compose up -d
docker compose exec -T -u dev agent dockercat-smoke
docker compose down
```

The last command preserves state volumes. Use disposable test state for recreation, SSH, and mount tests; never delete an operator's volumes to run a check. See [development](docs/development.md) and [validation](docs/validation.md) for overlay configuration and runtime regression commands. Portainer builds also need the Dockerfile, scripts, and configuration from the complete checkout.

Report evidence accurately:

| Evidence | What it establishes |
| --- | --- |
| Shell/Compose/static checks | Syntax, resolved configuration, and stated static policy assertions |
| Synthetic runtime checks | Built image behavior with disposable files, keys, and volumes |
| Manual account-holder tests | The specific subscription/API/MCP workflow and authenticated-state lifecycle actually exercised |
| Manual host/client tests | The actual hardware, Portainer endpoint, network, or remote client exercised |

CI must remain credential-free. Never put personal Claude or Mem credentials into tests, fixtures, workflow secrets, or public evidence. Do not claim live OAuth, ARM64, or a real deployment from a synthetic fixture.

## Maintain documentation

Update the canonical guide in `docs/` when behavior or commands change. Keep README navigation, examples, security limits, and roadmap support claims consistent. Wiki source in `wiki/` should provide concise introductions and link to those guides; follow the [wiki publication procedure](docs/wiki-publishing.md) after source review instead of publishing competing copies.
