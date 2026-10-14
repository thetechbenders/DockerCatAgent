#!/usr/bin/env sh
set -eu
test -d /workspace
test -d /home/dev
command -v claude >/dev/null
command -v git >/dev/null
command -v tmux >/dev/null
