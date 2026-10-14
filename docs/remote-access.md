# SSH and persistent terminal operation

SSH is optional. The default Compose service publishes no ports. Enabling SSH runs a root daemon inside the container so it can authenticate and switch to `dev`; development shells remain non-root. Read the [security model](security.md) before enabling access.

## Authorized keys and loopback binding

Create a dedicated host file containing the **public** keys you authorize. Never copy private keys into the image, container or repository. Its parent directories and file must not be writable by unrelated users; use an operator-owned file with mode `0600`, and ensure SSH's strict ownership checks are satisfied. If the operator's host UID is neither root nor 1000, verify the bind file's ownership with the effective daemon; use a dedicated appropriately owned file rather than weakening strict checks.

Set these non-secret values in private `.env` on the Docker host:

```dotenv
SSH_AUTHORIZED_KEYS_FILE=/absolute/path/to/authorized_keys
SSH_BIND_ADDRESS=127.0.0.1
SSH_PORT=2222
OAUTH_CALLBACK_PORT=8765
```

`SSH_AUTHORIZED_KEYS_FILE` must already be a regular nonempty file, not a directory. From the complete checkout:

```sh
docker compose -f compose.yml -f compose.ssh.yml config -q
docker compose -f compose.yml -f compose.ssh.yml up -d
docker compose -f compose.yml -f compose.ssh.yml logs --tail 50 agent
```

Review logs locally for startup failure without sharing private paths. On the same host, connect using your client-held key:

```sh
ssh -p 2222 dev@127.0.0.1
```

If necessary, select a dedicated client key using `-i` and `-o IdentitiesOnly=yes`. Passwords, keyboard-interactive authentication, root login and other users are prohibited by the supplied configuration. A failed public-key login must not fall back to a password.

## Host identity and key changes

In SSH mode, an Ed25519 server key is generated into the persistent `ssh_hostkeys` volume on first start. Verify its public fingerprint through the host console before accepting a client's first-connect prompt:

```sh
docker compose -f compose.yml -f compose.ssh.yml exec -T -u root agent \
  ssh-keygen -lf /etc/ssh/dockercat-hostkeys/ssh_host_ed25519_key.pub
```

Recreate the container and confirm the fingerprint stays the same. If a client reports changed identity, stop and confirm the Docker endpoint, Compose project and actual key before altering `known_hosts`. Do not automatically suppress host-key checking. Replacing authorized public keys changes who can log in; it is separate from rotating the server's host key. Make changes through the protected host file, verify new access, and retire old access deliberately.

## VPN and remote clients

Loopback binding reaches only the Docker host. For a remote client, choose a specific trusted VPN/private-interface address in `SSH_BIND_ADDRESS`, and apply host firewall/VPN policy. DockerCatAgent does not install a VPN or firewall. Do not switch to `0.0.0.0` merely to make a remote connection work.

Laptop, tablet and phone clients need a terminal, protected SSH private key, host-key verification and access to the trusted host interface. Check terminal resizing, reconnect behavior, keyboard support for `Ctrl-b`, UTF-8 and the chosen tmux workflow on the actual client. No mobile-client compatibility matrix has been certified. Use a device lock and revoke lost-device keys promptly.

## tmux and observation

From a normal `dev` shell:

```sh
tmux new-session -A -s work
```

Run Claude and other tools inside that session. `Ctrl-b`, then `d` detaches; the tmux command reconnects while the container remains running. An additional terminal can observe:

```sh
tmux attach-session -r -t work
```

Read-only attachment prevents input through that attached tmux client. It is **not** a separate viewer account: someone with the same SSH shell can open a writable client, read credentials or modify files. Use it only with people already trusted for that account. Restarts and recreation end tmux processes; volumes preserve files, not sessions.

## Restricted OAuth callback forwarding

The SSH template permits local TCP forwarding only to `localhost` or `127.0.0.1` at `OAUTH_CALLBACK_PORT`, default 8765. It rejects other destinations, remote forwarding, Unix-socket forwarding, SSH-agent forwarding, X11 and tunnels. This is a callback transport mechanism, not general proxy access.

For a browser on the client and an MCP callback listener inside the container, keep a dedicated client terminal open:

```sh
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:8765:localhost:8765 \
  -p 2222 dev@127.0.0.1
```

For remote access replace the final host with the selected trusted Docker-host address. The first `127.0.0.1:8765` binds the **client's** listener privately; the `localhost:8765` destination is resolved inside the container. Use the same port for the MCP client's callback configuration, `.env` and tunnel. Use a canonical decimal integer from 1024 through 65535, without leading zeroes; other forms are rejected by startup validation.

Run the provider's OAuth flow in a second authenticated `dev` shell. Leave the tunnel active until completion, then close it. A successful tunnel command only proves a local listener was created; it does not prove that the provider accepted a redirect or that a container callback listener exists. `ExitOnForwardFailure` does not prove destination acceptance before a connection is attempted. Account-holder validation of Mem and Claude authentication remains separate.

## Effective configuration and troubleshooting

On the Docker host, inspect the generated runtime configuration:

```sh
docker compose -f compose.yml -f compose.ssh.yml exec -T -u root agent \
  /usr/sbin/sshd -T -f /run/sshd-dockercat.conf
```

Confirm the effective authentication restrictions and permitted callback destinations. Use actual connections for positive and negative tests; see [validation](validation.md). An empty key file, invalid callback port, mismatched bind ownership or lost host-key volume is a configuration problem to resolve, not a reason to relax authentication.

For failed connections see [troubleshooting](troubleshooting.md). For privacy when collecting logs see [diagnostics](diagnostics.md).
