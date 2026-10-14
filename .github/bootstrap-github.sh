#!/usr/bin/env bash
# Maintainer metadata reconciliation; authenticated gh and jq required.
# Dry-run by default. Never removes metadata or changes milestone state/dates.
set -euo pipefail
repo="${REPO:-thetechbenders/DockerCatAgent}"
cd "$(dirname "$0")/.."
command -v jq >/dev/null

if [[ "${APPLY:-0}" != "1" ]]; then
  echo "DRY RUN: would upsert and verify labels and milestone descriptions in $repo"
  jq -r '.[] | "label: \(.name) #\(.color)"' .github/labels.json
  jq -r '.[] | "milestone: \(.title)"' .github/milestones.json
  echo "To apply: APPLY=1 REPO=$repo .github/bootstrap-github.sh"
  exit 0
fi

command -v gh >/dev/null
gh auth status >/dev/null
while IFS= read -r label; do
  name="$(jq -r '.name' <<<"$label")"
  gh label create "$name" --repo "$repo" \
    --color "$(jq -r '.color' <<<"$label")" \
    --description "$(jq -r '.description' <<<"$label")" --force
done < <(jq -c '.[]' .github/labels.json)

live_labels="$(gh api --paginate "repos/$repo/labels?per_page=100" | jq -s 'add')"
jq -e -n --argjson actual "$live_labels" --slurpfile expected .github/labels.json '
  all($expected[0][]; . as $e |
    any($actual[]; .name == $e.name and
      (.color | ascii_downcase) == ($e.color | ascii_downcase) and
      .description == $e.description))' >/dev/null

while IFS= read -r milestone; do
  title="$(jq -r '.title' <<<"$milestone")"
  desc="$(jq -r '.description' <<<"$milestone")"
  matches="$(gh api --paginate "repos/$repo/milestones?state=all&per_page=100" |
    jq -s --arg title "$title" '[.[][] | select(.title == $title)]')"
  count="$(jq 'length' <<<"$matches")"
  if [[ "$count" -gt 1 ]]; then
    echo "Multiple milestones named $title; reconcile manually" >&2
    exit 1
  elif [[ "$count" -eq 1 ]]; then
    number="$(jq -r '.[0].number' <<<"$matches")"
    gh api --method PATCH "repos/$repo/milestones/$number" -f description="$desc" >/dev/null
  else
    number="$(gh api --method POST "repos/$repo/milestones" \
      -f title="$title" -f description="$desc" --jq '.number')"
  fi
  gh api "repos/$repo/milestones/$number" |
    jq -e --arg title "$title" --arg desc "$desc" \
      '.title == $title and .description == $desc' >/dev/null
done < <(jq -c '.[]' .github/milestones.json)
echo "GitHub labels and milestones verified; issue assignment is a separate triage step"
