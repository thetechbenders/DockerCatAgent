# Personal Claude instructions

Keep personal instructions in the persistent container home, not in the public image or this repository. Claude's user-level instructions use `~/.claude/CLAUDE.md`; consult [Claude's current memory/instructions guide](https://code.claude.com/docs/en/memory) for version-specific loading and project overrides.

Inside a `dev` shell:

```sh
mkdir -p /home/dev/.claude
chmod 700 /home/dev/.claude
nano /home/dev/.claude/CLAUDE.md
```

Useful generic guidance describes the user's review expectations: inspect relevant files, explain changes, use focused branches, verify outcomes, and ask before an irreversible external action. Tailor it privately to your workflow. Do not put tokens, private note identifiers, personal network addresses or provider account details in instructions that might enter prompts or logs.

Personal instructions survive normal recreation because the whole home is persistent. A repository's project instructions may also affect sessions; inspect them before trusting a project. These text files do not constrain filesystem or provider authorization. Enforce permissions through mounts, identities, provider grants and tool approvals, then use prose to state intent.

No maintainer personality or private standing orders are included in the distributed runtime. See [authentication-state lifecycle](architecture.md#authentication-state-lifecycle) and [security boundaries](security.md).
