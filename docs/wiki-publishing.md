# Reviewed GitHub Wiki synchronization

`docs/` is the canonical operator/development source. `wiki/` contains concise landing and navigation pages reviewed in the same PR as the guides. The [official GitHub Wiki](https://github.com/thetechbenders/DockerCatAgent/wiki) publishes this navigation separately, with canonical links pinned to the approved source commit.

Publication is a separate maintainer action after source review and explicit publication authorization. Preparing these files or a successful CI run does not authorize publishing an unreviewed wiki.

## Verified publication

- **Publication date:** `2026-10-14` (UTC).
- **Reviewed source:** `db1852e53486a6b1c84a699d61aeff31ac099011`, merged through [PR #23](https://github.com/thetechbenders/DockerCatAgent/pull/23).
- **Reviewed-head CI:** [run 38602142634](https://github.com/thetechbenders/DockerCatAgent/actions/runs/38602142634) passed on reviewed PR head `d96fb2d4aa9770749e81752a75fbdf6f375a56e5`.
- **Merged-source CI:** [run 38604403435](https://github.com/thetechbenders/DockerCatAgent/actions/runs/38604403435) passed both jobs on the published source SHA.
- **Prior wiki HEAD:** `9dadff7b1ef4b75b087d7da6022529fb7fdf3544`; only its placeholder Home page existed, so no unrelated pages were displaced.
- **Published wiki commit:** `53c9055b707522e93d4e97ccc27bb1b375b1274c` on `master`.
- **Published Markdown files:** `Home.md`, `Getting-Started.md`, `Architecture.md`, `Remote-Operation.md`, `Integrations.md`, `Operations.md`, `Development.md`, `Security.md`, `Roadmap.md`, `_Sidebar.md`, `_Footer.md`.
- **Evidence:** four exporter regression tests passed; all 11 export hashes, 75 source-pinned links, 37 meaningful heading anchors and 44 cross-wiki links were checked. The exact wiki diff contained ten additions and replacement of the placeholder Home, with no unrelated deletion. `git diff --check` and remote commit read-back passed. Public HTTP/HTML checks verified the landing page, all nine topic pages with their sidebar/footer, and 21 source-pinned canonical document targets. The `_Sidebar` and `_Footer` URL routes redirect to Home and their content was verified in the rendered widgets. The export manifest was retained as review evidence and was not published as a wiki page. See [#14](https://github.com/thetechbenders/DockerCatAgent/issues/14) for the publication record and any remaining limitations.

Techbenders maintainers with existing wiki write access own future updates. Review documentation changes in a repository PR, select the approved merged source commit, then follow the export/review/synchronization checklist below under explicit publication authorization. Record each successful source/wiki commit pair and public verification in the tracking issue or a repository documentation PR. If canonical guides change after publication, the wiki continues to show its pinned source until the next reviewed synchronization. In particular, this publication record is a follow-up documentation change; the published wiki remains pinned to the earlier approved SHA until a later separately approved synchronization. Historical audit reports describe their own earlier work and are not current publication status.

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
python3 -m unittest discover -s tests -p 'test_wiki_export.py'
python3 scripts/export-wiki.py --ref "$approved_sha" --output ./wiki-export
```

Confirm that `origin/main` contains the reviewed publication changes and no intervening unreviewed wiki changes before using it as `approved_sha`; current main alone is not approval. `wiki-export/` must not already exist. The script validates source links against the approved Git tree, rewrites repository-relative canonical links to permalinks at the approved SHA, rewrites cross-wiki links into wiki page URLs, and refuses missing destinations. The export contains the 11 Markdown pages plus `manifest.json` with the source SHA and content hashes. The manifest is **review evidence only** and must not be copied into the public wiki repository.

Before publishing, inspect each generated page and its links, run `python3 -m unittest discover -s tests -p 'test_wiki_export.py'`, and compare the manifest against the approved commit. Exporting does **not** clone, edit or push the wiki. If the wiki remote has changed, review conflicts first rather than forcing a blind mirror.

**The merged foundation commit** `7906169027df61a307f4c0cacf11273517ea0495` is a historical baseline, not an automatic publishing target. For the post-merge wiki documentation corrections, use the new **reviewed and merged** source commit rather than that older baseline.

## Review and synchronize the separate repository

An authenticated maintainer with wiki write permission can clone it to a separate directory:

```sh
git clone https://github.com/thetechbenders/DockerCatAgent.wiki.git ../DockerCatAgent.wiki
```

If the clone already exists, inspect its status and fetch current remote state before a non-destructive fast-forward update. Check the remote default branch rather than assuming it matches the code repository's `main`. Read current pages and resolve content conflicts. Copy only the prepared page files after that review; do not use a deletion-based mirror.

```sh
cp ./wiki-export/*.md ../DockerCatAgent.wiki/
git -C ../DockerCatAgent.wiki diff --check
git -C ../DockerCatAgent.wiki diff
```

The wiki repository has no ordinary source PR review gate. Require the source PR and export diff to be reviewed before any wiki commit/push. Once separately authorized, commit using the established identity with a message recording the full source SHA, push without force, then read back the live Home/sidebar/pages and canonical document links. If permission or source approval is missing, stop at the prepared export and report that limitation.

A failed or partial sync is not a published documentation success. Record the published wiki commit and source SHA in repository governance documentation after verification. No automated sync, broad token grant or wiki publication is installed by this guide.

## Corrections and rollback

Techbenders maintainers review corrections in the source repository first. A wiki publisher with existing write access exports an explicitly approved source, inspects the current wiki and diff, commits normally and verifies both Git read-back and public rendering. If a rollback is needed, select an approved prior source commit and export it to a fresh directory; review the replacement pages against the current wiki, preserve unrelated pages, and commit the correction as a new wiki commit. Do not reset, delete-mirror or force-push wiki history. Record the source/wiki SHA pair, reason and public verification result. A prior source that lacks the exporter requires the reviewed exporter from a later approved checkout; the export reference must still be the selected approved prior source. Rollback is a separately authorized publication action.
