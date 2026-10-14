# Operations and recovery

Baseline lifecycle: build, run, exec, attach tmux, rebuild, recreate, validate persistence and only then consider backups. Do not confuse named volumes with process snapshots.

Future runbooks: backup/restore with checksums, rotation of auth/SSH host identity, storage migration, safe removal and upgrade/rollback.