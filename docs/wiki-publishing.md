# Reviewed GitHub Wiki synchronization

`docs/` is the canonical operator/development source. `wiki/` contains concise landing and navigation pages reviewed in the same PR as the guides. The separate GitHub Wiki is enabled and was initialized with a placeholder Home page when inspected on 2026-10-14. The prepared pages in this branch have **not** been synchronized there.

Publication is a separate maintainer action after source review and explicit publication authorization. Preparing these files or a successful CI run does not authorize publishing an unreviewed wiki.

## Single-source policy

- Edit long-form procedures in `docs/`; wiki pages introduce topics and link to those procedures.
- Edit navigational wiki content in `wiki/` through repository PRs, not directly in the wiki UI.
- Export canonical document links to an approved **commit SHA**, so the published wiki has an auditable source and never silently points at a moving unreviewed branch.
- Every synchronization records the approved source SHA in the wiki commit message. Future synchronization updates links to the newly approved source.
- Inspect current wiki contents before copying. Preserve unrelated maintainer-authored pages and resolve conflicting edits through review; never force-push or blindly delete them.

The source-tree links use `../docs/` and sibling `.md` filenames for repository review. Those paths do not work unchanged in the separate wiki repository. Export rewrites canonical links to the approved main repository commit and sibling links to GitHub Wiki URLs.

## Prepare an export without publishing

After choosing the reviewed source SHA, run the following in Bash from a clean complete source checkout. Replace the sample `REVIEWED_COMMIT_SHA` with the actual approved commit, not a branch name. This creates only temporary local files:

```bash
set -euo pipefail
approved_ref='REVIEWED_COMMIT_SHA'
git cat-file -e "$approved_ref^{commit}"
staging_dir="$(mktemp -d)"
git archive "$approved_ref" wiki | tar -x -C "$staging_dir"
python3 - "$staging_dir" "$approved_ref" <<'PYTHON'
from pathlib import Path
import re
import sys

stage = Path(sys.argv[1])
source_sha = sys.argv[2]
if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
    raise SystemExit("Use the full approved commit SHA")
source_url = f"https://github.com/thetechbenders/DockerCatAgent/blob/{source_sha}/"
wiki_url = "https://github.com/thetechbenders/DockerCatAgent/wiki/"
output = stage / "export"
output.mkdir()

def rewrite(match):
    target = match.group(1)
    if target.startswith("../"):
        target = source_url + target[3:]
    elif ".md" in target and "/" not in target.split("#", 1)[0]:
        page, _, anchor = target.partition("#")
        target = wiki_url + page.removesuffix(".md")
        if anchor:
            target += "#" + anchor
    return "](" + target + ")"

for page in (stage / "wiki").glob("*.md"):
    text = re.sub(r"\]\(([^)]+)\)", rewrite, page.read_text())
    (output / page.name).write_text(text)
print(f"Prepared {len(list(output.glob('*.md')))} pages in {output}")
PYTHON
```

Inspect the export: sibling navigation, sidebar, canonical links, code formatting and source SHA. The exporter intentionally handles this wiki's simple inline Markdown links; new link formats need review before use. No repository file, wiki remote or production service is changed by export.

## Review and synchronize the separate repository

An authenticated maintainer with wiki write permission can clone it to a separate directory:

```sh
git clone https://github.com/thetechbenders/DockerCatAgent.wiki.git ../DockerCatAgent.wiki
```

If the clone already exists, inspect its status and fetch current remote state before a non-destructive fast-forward update. Check the remote default branch rather than assuming it matches the code repository's `main`. Read current pages and resolve content conflicts. Copy only the prepared page files after that review; do not use a deletion-based mirror.

```sh
cp "$staging_dir/export/"*.md ../DockerCatAgent.wiki/
git -C ../DockerCatAgent.wiki diff --check
git -C ../DockerCatAgent.wiki diff
```

The wiki repository has no ordinary source PR review gate. Require the source PR and export diff to be reviewed before any wiki commit/push. Once separately authorized, commit using the established identity with a message recording the full source SHA, push without force, then read back the live Home/sidebar/pages and canonical document links. If permission or source approval is missing, stop at the prepared export and report that limitation.

A failed or partial sync is not a published documentation success. Record the published wiki commit and source SHA in repository governance documentation after verification. No automated sync, broad token grant or wiki publication is installed by this guide.
