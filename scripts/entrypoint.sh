#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" != "sshd" ]]; then
  exec "$@"
fi
if [[ "$(id -u)" -ne 0 ]]; then
  echo "SSH mode needs root for privilege separation and non-root login" >&2
  exit 1
fi
port="${OAUTH_CALLBACK_PORT:-8765}"
if [[ ! "$port" =~ ^[1-9][0-9]{3,4}$ ]] || (( port < 1024 || port > 65535 )); then
  echo "OAUTH_CALLBACK_PORT must be decimal, 1024..65535, without leading zeroes" >&2
  exit 2
fi
keys=/etc/ssh/dockercat-hostkeys
mkdir -p "$keys" /run/sshd
# Minimal Debian containers may omit utmp. OpenSSH records PTY logins there;
# keep it runtime-only and never world-writable. Do not replace existing data.
if [[ ! -e /run/utmp ]]; then
  install -o root -g utmp -m 0664 /dev/null /run/utmp
fi
chmod 0700 "$keys"
private_key="$keys/ssh_host_ed25519_key"
public_key="$private_key.pub"
if [[ ! -f "$private_key" ]]; then
  (umask 077; ssh-keygen -q -t ed25519 -N '' -f "$private_key")
fi
# A restored private key may have overly broad permissions. Fix those *before*
# asking ssh-keygen to read it; ssh-keygen refuses modes such as 0644.
chmod 0600 "$private_key"
if [[ -L "$public_key" || ( -e "$public_key" && ! -f "$public_key" ) ]]; then
  echo "SSH host public key must be a regular non-symlink file" >&2
  exit 1
fi
if [[ ! -s "$public_key" ]]; then
  # An absent or zero-byte sidecar must never be left as a broken artifact.
  # Build alongside the target, then replace atomically after success.
  temporary_public="$(mktemp "$keys/.ssh_host_ed25519_key.pub.XXXXXX")"
  if ! ssh-keygen -y -f "$private_key" > "$temporary_public"; then
    rm -f -- "$temporary_public"
    echo "Unable to recover SSH host public key" >&2
    exit 1
  fi
  chmod 0644 "$temporary_public"
  mv -f -- "$temporary_public" "$public_key"
fi
chmod 0644 "$public_key"
if [[ ! -f /home/dev/.ssh/authorized_keys || ! -s /home/dev/.ssh/authorized_keys ]]; then
  echo "SSH authorized_keys must be a nonempty regular file" >&2
  exit 3
fi
 # The dev-owned .ssh may contain user-controlled symlinks: never chmod it as root.
sed "s/@OAUTH_CALLBACK_PORT@/$port/g" /etc/ssh/sshd_config.dockercat.template > /run/sshd-dockercat.conf
/usr/sbin/sshd -t -f /run/sshd-dockercat.conf
exec /usr/sbin/sshd -D -e -f /run/sshd-dockercat.conf
