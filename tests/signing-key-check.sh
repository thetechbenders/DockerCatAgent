#!/usr/bin/env bash
# Synthetic GPG fixtures; no actual package signing material or provider login.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export GNUPGHOME="$tmp/gnupg"
install -d -m 0700 "$GNUPGHOME"
gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key \
  'DockerCat Fixture One <first@example.invalid>' ed25519 sign 0 >/dev/null 2>&1
first="$(gpg --batch --with-colons --list-keys 'DockerCat Fixture One' | awk -F: '$1=="fpr" {print $10; exit}')"
gpg --batch --armor --export 'DockerCat Fixture One' > "$tmp/first.asc"
checker="$root/scripts/verify-signing-key.sh"
sh "$checker" "$tmp/first.asc" "$first"
gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key \
  'DockerCat Fixture Two <second@example.invalid>' ed25519 sign 0 >/dev/null 2>&1
cp "$tmp/first.asc" "$tmp/two.asc"
gpg --batch --armor --export 'DockerCat Fixture Two' >> "$tmp/two.asc"
if sh "$checker" "$tmp/two.asc" "$first" >/dev/null 2>&1; then
  echo "FAIL: appended public key accepted" >&2; exit 1
fi
if sh "$checker" "$tmp/first.asc" 0000000000000000000000000000000000000000 >/dev/null 2>&1; then
  echo "FAIL: incorrect fingerprint accepted" >&2; exit 1
fi
printf '%s\n' 'not valid OpenPGP' > "$tmp/invalid.asc"
if sh "$checker" "$tmp/invalid.asc" "$first" >/dev/null 2>&1; then
  echo "FAIL: invalid keyring accepted" >&2; exit 1
fi
echo "PASS signing-key trust: correct, appended, wrong and malformed fixtures"
