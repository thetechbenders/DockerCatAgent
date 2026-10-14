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

A reviewed source commit must be **merged and approved** before its content is published. The exporter reads the exact Git commit, not an uncommitted working tree or moving branch. From a complete checkout, provide the **full 40-character commit SHA** approved for publication:

```bash
git fetch origin main
approved_sha="$(git rev-parse --verify origin/main^{commit})"
python3 scripts/export-wiki.py --ref "$approved_sha" --output ./wiki-export
```

`wiki-export/` must not already exist. The script validates source links against the approved Git tree, rewrites repository-relative canonical links to permalinks at the approved SHA, rewrites cross-wiki links into wiki page URLs, and refuses missing destinations. The export contains the 11 Markdown pages plus `manifest.json` with the source SHA and content hashes. The manifest is **review evidence only** and must not be copied into the public wiki repository.

Before publishing, inspect each generated page and its links, run `python3 -m unittest discover -s tests -p 'test_wiki_export.py'`, and compare the manifest against the approved commit. Exporting does **not** clone, edit or push the wiki. If the wiki remote has changed, review conflicts first rather than forcing a blind mirror.

**The merged foundation commit** `7906169027df61a307f4c0cacf11273517ea0495` is a historical baseline, not an automatic publishing target. For the post-merge wiki documentation corrections, use the new **reviewed and merged** source commit rather than that older baseline.

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
