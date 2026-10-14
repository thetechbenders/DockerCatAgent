#!/usr/bin/env python3
"""Export reviewed wiki source as publishable Markdown pinned to a Git commit.

This program never connects to, alters, or publishes the separate GitHub wiki.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import tempfile

SOURCE_REPO = "https://github.com/thetechbenders/DockerCatAgent"
WIKI_BASE = SOURCE_REPO + "/wiki/"
LINK_RE = re.compile(r"\]\(([^)]+)\)")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")


def git(root: Path, *args: str) -> bytes:
    command = ["git", "-C", str(root), *args]
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode:
        raise ValueError(f"Git command failed: {args[0]} (exit {result.returncode}): "
                         + result.stderr.decode(errors="replace").strip())
    return result.stdout


def export(root: Path, source_ref: str, output: Path) -> tuple[str, int]:
    if not SHA_RE.fullmatch(source_ref):
        raise ValueError("--ref must be a complete 40-character reviewed Git commit SHA")
    sha = git(root, "rev-parse", "--verify", f"{source_ref}^{{commit}}").decode().strip()
    if sha != source_ref:
        raise ValueError("Ref must name the actual reviewed commit, not an alias")
    names = [name for name in git(root, "ls-tree", "-r", "--name-only", sha, "wiki/")
             .decode().splitlines() if name.endswith(".md") and name.count("/") == 1]
    if "wiki/Home.md" not in names or "wiki/_Sidebar.md" not in names:
        raise ValueError("Wiki source must contain Home.md and _Sidebar.md")
    pages = {posixpath.basename(name): git(root, "show", f"{sha}:{name}").decode("utf-8")
             for name in names}
    if output.exists() or output.is_symlink():
        raise ValueError(f"Refusing to overwrite existing export destination: {output}")
    parent = output.parent
    if not parent.is_dir():
        raise ValueError(f"Export parent directory does not exist: {parent}")

    def rewrite_target(target: str, page: str) -> str:
        address, marker, anchor = target.partition("#")
        if target.startswith(("https://", "http://", "mailto:")) or not address:
            return target
        if address.startswith("../"):
            normalized = posixpath.normpath(posixpath.join("wiki", address))
            if normalized == ".." or normalized.startswith("../"):
                raise ValueError(f"{page}: link escapes source repository: {target}")
            git(root, "cat-file", "-e", f"{sha}:{normalized}")
            rewritten = f"{SOURCE_REPO}/blob/{sha}/{normalized}"
        elif "/" not in address and address.endswith(".md"):
            if address not in pages:
                raise ValueError(f"{page}: wiki destination does not exist: {target}")
            rewritten = WIKI_BASE + address[:-3]
        else:
            raise ValueError(f"{page}: unsupported relative link: {target}")
        return rewritten + ("#" + anchor if marker else "")

    exported = {}
    for name, original in sorted(pages.items()):
        rewritten = LINK_RE.sub(lambda m: "](" + rewrite_target(m.group(1), name) + ")", original)
        if "](../" in rewritten or re.search(r"\]\([A-Za-z0-9_-]+\.md(?:#|\))", rewritten):
            raise ValueError(f"{name}: unresolved wiki/source link remains")
        exported[name] = rewritten.encode("utf-8")

    manifest = {"source_sha": sha, "repository": SOURCE_REPO,
                "pages": {name: hashlib.sha256(payload).hexdigest()
                          for name, payload in exported.items()}}
    # Validate all links before creating destination. Stage then atomically move.
    with tempfile.TemporaryDirectory(prefix=".wiki-export-stage-", dir=parent) as staging:
        staging_dir = Path(staging)
        for name, payload in exported.items():
            (staging_dir / name).write_bytes(payload)
        (staging_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.rename(staging_dir, output)
    return sha, len(exported)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="approved 40-character source commit SHA")
    parser.add_argument("--output", required=True, type=Path, help="new export directory")
    args = parser.parse_args()
    try:
        sha, count = export(Path(__file__).resolve().parent.parent,
                            args.ref, args.output.resolve())
    except (OSError, ValueError) as error:
        parser.exit(1, f"Wiki export failed: {error}\n")
    print(f"Exported {count} wiki pages from {sha} to {args.output}")
    print("Review manifest.json; copy only *.md files to the separate wiki Git repository.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
