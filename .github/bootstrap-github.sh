#!/usr/bin/env bash
# Optional maintainer-only metadata bootstrap. Requires authenticated gh and jq.
# Dry-run by default. APPLY=1 writes labels and missing milestones.
set -euo pipefail
repo="${REPO:-thetechbenders/DockerCatAgent}"
cd "$(dirname "$0")/.."

if [[ "${APPLY:-0}" != "1" ]]; then
  echo "DRY RUN: would upsert labels and create absent milestones in $repo"
  jq -r '.[] | "label: \(.name) #\(.color)"' .github/labels.json
  jq -r '.[] | "milestone: \(.title)"' .github/milestones.json
  echo "To apply: APPLY=1 REPO=$repo .github/bootstrap-github.sh"
  exit 0
fi

command -v gh >/dev/null
command -v jq >/dev/null
gh auth status >/dev/null
jq -c '.[]' .github/labels.json | while IFS= read -r label; do
  name="$(jq -r '.name' <<<"$label")"
  color="$(jq -r '.color' <<<"$label")"
  desc="$(jq -r '.description' <<<"$label")"
  gh label create "$name" --repo "$repo" --color "$color" --description "$desc" --force
done

jq -c '.[]' .github/milestones.json | while IFS= read -r milestone; do
  title="$(jq -r '.title' <<<"$milestone")"
  desc="$(jq -r '.description' <<<"$milestone")"
  if gh api --paginate "repos/$repo/milestones?state=all&per_page=100" --jq '.[].title' | grep -Fxq "$title"; then
    echo "Milestone exists: $title"
  else
    gh api --method POST "repos/$repo/milestones" -f title="$title" -f description="$desc" >/dev/null
    echo "Created milestone: $title"
  fi
done
echo "GitHub metadata bootstrap complete"
