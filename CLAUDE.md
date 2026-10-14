# DockerCatAgent engineering conventions

- Keep the project generic and free of maintainer-specific accounts, infrastructure, or personas.
- Make Compose authoritative; optional overlays must leave the default safe path alone.
- Use only official, documented Claude Code distribution and supported authentication.
- Protect persistent home and workspace as potentially secret-bearing volumes.
- Never embed credentials, vault content, authorization tokens, SSH private keys, or account-specific instructions.
- No privileged containers, Docker socket access, host networking, or public SSH by default.
- Treat SSH forwarding and all externally mounted data as security-sensitive interfaces.
- Make shell scripts narrow and auditable; validate inputs and quote expansions.
- Add negative tests for authorization and mount changes.
- Separate static, simulated, container, and authenticated-user validation results.
- No auto-merge, tag, release, deployment, or registry publishing without owner authorization.

This file defines neutral repository development conventions, not an agent personality.