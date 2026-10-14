#!/usr/bin/env bash
set -euo pipefail
claude --version
git --version
tmux -V
id
test "$(id -u)" = 1000
test "$(id -g)" = 1000
f="$(mktemp /workspace/dockercat-smoke.XXXXXX)"
printf 'persistence probe\n' > "$f"
test -s "$f"
rm -f "$f"
test -w /workspace
test -w /home/dev
echo "Baseline smoke passed; login and actual recreation require separate checks"
