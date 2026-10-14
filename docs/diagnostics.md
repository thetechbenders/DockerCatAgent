# Privacy-preserving logs and diagnostics

There is no automated diagnostic collector. Run the smallest relevant checks and inspect output privately before sharing it. Home and workspace can contain credentials, prompts, source code, provider metadata and private paths.

## A minimal local inventory

From the checkout on the Docker host, with the same overlays used to start it:

```sh
git rev-parse HEAD
docker version --format '{{.Server.Version}}'
docker compose version
docker info --format '{{.Architecture}}'
docker compose config -q
docker compose ps
docker compose exec -T -u dev agent id
docker compose exec -T -u dev agent claude --version
docker compose exec -T -u dev agent git --version
docker compose exec -T -u dev agent tmux -V
docker compose exec -T -u dev agent sh -c 'test -w /workspace && test -w /home/dev'
```

`config -q` validates without printing interpolated host paths or settings. `docker compose ps` can still disclose project/network information; redact it for public reports. Record architecture, versions, selected overlays and expected versus observed behavior. Avoid broad environment dumps, full `docker inspect`, complete home listings or generated support bundles.

## Logs

```sh
docker compose logs --tail 50 agent
```

The base mostly sleeps, so daemon logs are not a transcript of interactive Claude sessions. SSH mode logs connection/authentication events and can contain client addresses and usernames. Review locally and redact private data. Do not capture more log history merely to fill an issue report.

Do not publish tokens, API keys, private keys, OAuth URLs/query strings, vault contents, raw `claude mcp get` output, shell history, account names or personal paths. A package inventory or stack trace may also reveal private context. Use harmless fixtures when reproducing a defect; preserve original evidence privately if it is needed for security reporting.

## Focused checks

| Symptom | Safe first check |
| --- | --- |
| Build fails | Exit status and failing package/TLS step, with secrets and private proxy details redacted |
| Container unhealthy | Confirm command availability and directories; do not infer an account failure from health alone |
| Permission denied | `id` and ownership/mode of the specific affected path; no recursive host chmod |
| SSH fails | Host-key fingerprint, protected public-key file and effective sshd configuration |
| OAuth callback fails | Exact configured ports, tunnel lifetime and provider error category; exclude callback URL/token |
| Vault unavailable | Chosen overlay and mount metadata, then a disposable fixture test |
| State appears lost | Docker endpoint, project and volume metadata, not credential-file contents |

Account and security incidents need [private security reporting](../SECURITY.md), not a public credential-bearing reproduction. Future automated diagnostics must minimize collection, redact by default and require an explicit operator decision to export data.
