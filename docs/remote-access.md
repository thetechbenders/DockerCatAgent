# SSH and persistent terminal operations

The base container has no published ports. SSH must be enabled with an explicit Compose overlay and a user-supplied authorized_keys file of **public** keys. Bind host port 2222 to 127.0.0.1 by default, or a specifically chosen VPN/private interface. Do not publish SSH on the public internet by default. Store SSH host keys in a persistent volume; verify their fingerprint.

Only the non-root development user may log in. Disable passwords, keyboard-interactive and root login. For Mem and other OAuth clients, allow only SSH local TCP forwarding to the chosen callback port, not generic forwarding. Other SSH features, including remote forwarding and SSH-agent forwarding, should remain disabled.

Use tmux new-session -A -s work and tmux attach-session -r -t work for a read-only terminal *view*. Read-only tmux does not prevent a user who can open a normal shell from modifying files. An SSH login credential is not a separate viewer role.

For a laptop browser and a container OAuth callback on 8765, the intended local tunnel is: ssh -N -L 8765:localhost:8765 -p 2222 dev@127.0.0.1. The SSH daemon must permit exactly that destination. Change the destination host to the Docker host's trusted VPN address for remote use. Actual OAuth redirect/callback behavior must be validated with the provider and client.