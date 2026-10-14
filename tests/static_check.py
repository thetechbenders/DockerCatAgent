"""Dependency-light configuration checks; not a substitute for Docker runtime tests."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")

def check() -> None:
    default = read("compose.yml")
    ssh = read("compose.ssh.yml")
    ro = read("compose.obsidian.yml")
    rw = read("compose.obsidian-write.yml")
    sshd = read("config/sshd_config.template")
    entry = read("scripts/entrypoint.sh")
    dockerfile = read("Dockerfile")
    for forbidden in ("privileged:", "network_mode: host", "pid: host", "/var/run/docker.sock", "0.0.0.0:2222"):
        assert forbidden not in default, f"unsafe default setting: {forbidden}"
    assert "ports:" not in default, "default Compose must not publish ports"
    assert "cap_drop:" in default and "ALL" in default
    assert "no-new-privileges:true" in default
    assert 'user: "1000:1000"' in default
    assert "/workspace" in default and "/home/dev" in default
    assert "read_only: true" in ro
    assert "OBSIDIAN_VAULT_PATH" not in default
    assert "mcp.mem.ai" not in default
    assert "read_only: false" in rw
    assert "127.0.0.1" in ssh and "SSH_BIND_ADDRESS" in ssh
    assert "SSH_AUTHORIZED_KEYS_FILE" in ssh
    for required in ("PasswordAuthentication no", "KbdInteractiveAuthentication no", "PermitRootLogin no", "PubkeyAuthentication yes", "AllowUsers dev", "AllowTcpForwarding local", "GatewayPorts no", "PermitTunnel no", "PermitOpen localhost:@OAUTH_CALLBACK_PORT@ 127.0.0.1:@OAUTH_CALLBACK_PORT@"):
        assert required in sshd, f"SSH policy missing: {required}"
    assert '(( port < 1024 || port > 65535 ))' in entry
    assert "gpg --batch --show-keys --with-colons" in dockerfile
    assert "31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE" in dockerfile
    assert "USER dev" in dockerfile
    assert "docker compose down -v" in read("docs/installation.md"), "document destructive risk"
    paths = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    for path in paths:
        if path.name in (".env.example",) or path.suffix not in (".md", ".yml", ".yaml", ".sh", ".py"):
            continue
        content = path.read_text(encoding="utf-8")
        assert not re.search(r"(?i)(sk-ant-api03-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})", content), f"credential-looking string in {path}"
    print(f"Static checks passed ({len(paths)} checked files); runtime not tested")

if __name__ == "__main__":
    try:
        check()
    except (AssertionError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
