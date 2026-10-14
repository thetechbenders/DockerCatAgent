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
chmod 0700 "$keys"
if [[ ! -f "$keys/ssh_host_ed25519_key" ]]; then
  (umask 077; ssh-keygen -q -t ed25519 -N '' -f "$keys/ssh_host_ed25519_key")
elif [[ ! -f "$keys/ssh_host_ed25519_key.pub" ]]; then
  # Recover the public half without rotating the persistent private host identity.
  ssh-keygen -y -f "$keys/ssh_host_ed25519_key" > "$keys/ssh_host_ed25519_key.pub"
fi
chmod 0600 "$keys/ssh_host_ed25519_key"
chmod 0644 "$keys/ssh_host_ed25519_key.pub"
if [[ ! -f /home/dev/.ssh/authorized_keys || ! -s /home/dev/.ssh/authorized_keys ]]; then
  echo "SSH authorized_keys must be a nonempty regular file" >&2
  exit 3
fi
 # The dev-owned .ssh may contain user-controlled symlinks: never chmod it as root.
sed "s/@OAUTH_CALLBACK_PORT@/$port/g" /etc/ssh/sshd_config.dockercat.template > /run/sshd-dockercat.conf
/usr/sbin/sshd -t -f /run/sshd-dockercat.conf
exec /usr/sbin/sshd -D -e -f /run/sshd-dockercat.conf
