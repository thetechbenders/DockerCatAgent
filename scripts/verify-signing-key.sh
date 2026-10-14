#!/bin/sh
# Verify the expected primary key and reject additional trusted public keys.
# A signing subkey bound to the expected primary is not a second trust anchor.
set -eu
if [ "$#" -ne 2 ]; then echo "usage: verify-signing-key KEYRING EXPECTED_FINGERPRINT" >&2; exit 2; fi
keyring=$1
expected=$2
case "$expected" in ''|*[!0-9A-F]*) echo "invalid expected fingerprint" >&2; exit 2 ;; esac
metadata="$(gpg --batch --show-keys --with-colons -- "$keyring" 2>/dev/null)" || {
  echo "invalid signing keyring" >&2
  exit 1
}
printf '%s\n' "$metadata" | awk -F: -v expected="$expected" '
  $1=="pub" { pub++; want_fingerprint=1; next }
  $1=="sub" { want_fingerprint=0; next }
  $1=="fpr" && want_fingerprint { primary=$10; count++; want_fingerprint=0 }
  END { if (pub != 1 || count != 1 || primary != expected) exit 1 }
' || {
  echo "unexpected primary key or extra public keys in repository keyring" >&2
  exit 1
}
