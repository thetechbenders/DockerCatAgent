# Maintenance and Recovery

The [maintenance guide](../docs/maintenance.md) is the canonical lifecycle/runbook. Named volumes preserve files, not running processes, and are not a backup against host loss or deletion.

| Operation | Guide |
| --- | --- |
| Rebuild/recreate without changing the volume set | [Updating](../docs/maintenance.md#rebuilding-and-updating) |
| Record source/image/package versions | [Reproducibility limits](../docs/maintenance.md#build-reproducibility) |
| Identify actual attached volumes | [State inventory](../docs/maintenance.md#state-inventory) |
| Design and rehearse a credential-safe restore | [Draft backup/restore procedure](../docs/maintenance.md#backup-and-restoration-procedure-draft) |
| Tune and verify CPU/memory/process settings | [Resource limits](../docs/maintenance.md#resource-limits) |
| Handle missing sessions/auth/state/host keys | [Recovery triage](../docs/maintenance.md#recovery-triage) |
| Collect limited redacted evidence | [Logs and diagnostics](../docs/diagnostics.md) |
| Resolve common failures | [Troubleshooting](../docs/troubleshooting.md) |

The backup/restore procedure is a design requiring a disposable restore drill and an operator-chosen encrypted storage/key-management method. No one-command automated backup, migration, schema rollback or real-credential recovery is claimed.

Before upgrading, save work, preserve a protected pre-update backup and previous image identifier, then verify the new image against the same project/volume set. Older images do not automatically reverse configuration writes by newer clients. Authentication may still expire or need provider reauthorization.

Next: [Development](Development.md), [Security](Security.md). [Documentation home](Home.md).
