"""Credential-free Docker acceptance regressions; build dockercatagent:local first.

Uses disposable Compose projects, volumes, SSH keys, and a synthetic vault.
Does not validate account OAuth, hardware compatibility, or production deployment.
"""
from contextlib import contextmanager
import errno
import json
import os
from pathlib import Path
import pty
import select
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]


def run(*args, check=True, env=None, input_text=None):
    result = subprocess.run(args, cwd=ROOT, env=env, input=input_text, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if check and result.returncode:
        raise AssertionError(f"{' '.join(args)} failed:\n{result.stdout}{result.stderr}")
    return result


def interactive_client(args, commands, timeout=20):
    """Run the SSH client with a real controlling PTY, not piped fake input.

    Send commands after the first login prompt. Keep the local terminal open
    until SSH exits so remote shell exit status is not disrupted by pipe EOF.
    All credentials and server processes are disposable test fixtures.
    """
    pid, master = pty.fork()
    if pid == 0:
        os.chdir(ROOT)
        os.execvp(args[0], args)

    output = bytearray()
    submitted = False
    completed = False
    deadline = time.monotonic() + timeout
    try:
        while time.monotonic() < deadline:
            ready, _, _ = select.select([master], [], [], 0.15)
            if ready:
                try:
                    chunk = os.read(master, 65536)
                except OSError as error:
                    if error.errno == errno.EIO:
                        completed = True
                        break
                    raise
                if not chunk:
                    completed = True
                    break
                output.extend(chunk)
            if not submitted and b"dev@" in output and b"$ " in output:
                os.write(master, commands.encode())
                submitted = True
        if not completed:
            raise AssertionError("interactive SSH timed out; output: " +
                                 output.decode(errors="replace"))
    finally:
        os.close(master)
        if not completed:
            os.kill(pid, signal.SIGTERM)
        _, status = os.waitpid(pid, 0)
    if not submitted:
        raise AssertionError("SSH never presented interactive dev login prompt: " +
                             output.decode(errors="replace"))
    return subprocess.CompletedProcess(
        args, os.waitstatus_to_exitcode(status),
        stdout=output.decode(errors="replace"), stderr=""
    )


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@contextmanager
def project(overlay=None, extra_env=None):
    name = "dockercat-test-" + uuid.uuid4().hex[:10]
    env = {**os.environ, **(extra_env or {})}
    command = ["docker", "compose", "-p", name, "-f", "compose.yml"]
    if overlay:
        command += ["-f", overlay]

    def compose(*args, check=True):
        return run(*command, *args, check=check, env=env)

    try:
        compose("up", "-d", "--no-build")
        yield compose
    finally:
        # Only this generated test project's disposable volumes are removed.
        compose("down", "-v", "--remove-orphans")


def exec_dev(compose, code):
    return compose("exec", "-T", "-u", "dev", "agent", "bash", "-c", "set -euo pipefail; " + code).stdout.strip()


def baseline():
    with project() as compose:
        cid = compose("ps", "-q", "agent").stdout.strip()
        state = json.loads(run("docker", "inspect", cid).stdout)[0]
        assert state["Config"]["User"] == "1000:1000"
        assert not state["HostConfig"]["PortBindings"], "default ports published"
        assert state["HostConfig"]["CapDrop"] == ["ALL"]
        assert "no-new-privileges:true" in state["HostConfig"]["SecurityOpt"]
        assert "/vault" not in [m["Destination"] for m in state["Mounts"]]
        assert not any(m["Destination"] == "/var/run/docker.sock" for m in state["Mounts"])
        print(exec_dev(compose, "/usr/local/bin/dockercat-smoke"))
        exec_dev(compose, "/usr/local/bin/dockercat-healthcheck; "
                 "test ! -e /run/secrets/proxy_ca; test ! -e /etc/ssh/ssh_host_ed25519_key; "
                 "printf workspace > /workspace/.persist-probe; "
                 "printf '{\"testProbe\":true}' > /home/dev/.claude.json; "
                 "printf synthetic > /home/dev/.claude/.persist-probe; "
                 "tmux new-session -d -s persistence-probe")
        compose("up", "-d", "--no-build", "--force-recreate")
        exec_dev(compose, "test \"$(cat /workspace/.persist-probe)\" = workspace; "
                 "test \"$(cat /home/dev/.claude.json)\" = '{\"testProbe\":true}'; "
                 "test \"$(cat /home/dev/.claude/.persist-probe)\" = synthetic; "
                 "! tmux has-session -t persistence-probe 2>/dev/null")
        print("PASS baseline: non-root, tools, no exposure, synthetic home/workspace persistence; tmux terminates")


def entrypoint_inputs(directory):
    run("docker", "run", "--rm", "--user", "0:0", "dockercatagent:local", "bash", "-c",
        "set -eu; for port in 08765 999 65536 999999999999999999999 bogus; do "
        "status=0; OAUTH_CALLBACK_PORT=$port /usr/local/bin/dockercat-entrypoint sshd "
        ">/tmp/input-error 2>&1 || status=$?; test $status -eq 2; "
        "grep -q 'must be decimal' /tmp/input-error; done")
    result = run("docker", "run", "--rm", "--user", "0:0", "--mount",
                 f"type=bind,source={directory},target=/home/dev/.ssh/authorized_keys,readonly",
                 "dockercatagent:local", "sshd", check=False)
    assert result.returncode == 3 and "nonempty regular file" in result.stderr
    print("PASS SSH input validation: invalid/leading-zero/overflow ports and directory authorized_keys rejected")


def vault_checks(directory):
    vault = directory / "vault"
    vault.mkdir(mode=0o777)
    vault.chmod(0o777)  # synthetic fixture only; production permissions are operator-owned.
    (vault / "probe.md").write_text("synthetic vault probe\n")
    env = {"OBSIDIAN_VAULT_PATH": str(vault)}
    with project("compose.obsidian.yml", env) as compose:
        exec_dev(compose, "grep -q synthetic /vault/probe.md; "
                 "if touch /vault/write-probe 2>/tmp/vault-error; then exit 1; fi; "
                 "grep -qi 'Read-only file system' /tmp/vault-error")
    assert not (vault / "write-probe").exists()
    with project("compose.obsidian-write.yml", env) as compose:
        exec_dev(compose, "printf explicit-write > /vault/write-probe")
    assert (vault / "write-probe").read_text() == "explicit-write"
    print("PASS vault: absent by default, readable read-only mount denies writes, explicit writable mount succeeds")


def ssh_checks(directory):
    key = directory / "client"
    wrong_key = directory / "wrong-client"
    for path in (key, wrong_key):
        run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(path))
    authorized = directory / "authorized_keys"
    authorized.write_text(key.with_suffix(".pub").read_text())
    authorized.chmod(0o644)
    # Deliberately simulate a UID 1001 hosted-runner-owned file before normalizing.
    # StrictModes requires root/dev ownership; never relax the daemon policy.
    run("docker", "run", "--rm", "--user", "0:0", "--mount",
        f"type=bind,source={directory},target=/fixtures", "dockercatagent:local",
        "sh", "-ec", "chown 1001:1001 /fixtures/authorized_keys; "
        "test \"$(stat -c %u /fixtures/authorized_keys)\" = 1001; "
        "chown 1000:1000 /fixtures/authorized_keys")
    assert authorized.stat().st_uid == 1000
    port = free_port()
    env = {"SSH_AUTHORIZED_KEYS_FILE": str(authorized), "SSH_PORT": str(port),
           "OAUTH_CALLBACK_PORT": "8765", "SSH_BIND_ADDRESS": "127.0.0.1"}
    known_hosts = directory / "known_hosts"

    def client(identity=key, user="dev"):
        return ["ssh", "-F", "/dev/null", "-i", str(identity), "-p", str(port),
                "-o", "IdentitiesOnly=yes", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
                "-o", "StrictHostKeyChecking=accept-new", "-o", f"UserKnownHostsFile={known_hosts}",
                f"{user}@127.0.0.1"]

    with project("compose.ssh.yml", env) as compose:
        cid = compose("ps", "-q", "agent").stdout.strip()
        state = json.loads(run("docker", "inspect", cid).stdout)[0]
        assert state["HostConfig"]["PortBindings"]["2222/tcp"] == [
            {"HostIp": "127.0.0.1", "HostPort": str(port)}
        ], "SSH host publication must use the requested loopback bind"
        # A listening daemon does not prove successful privilege separation/login.
        for attempt in range(30):
            result = run(*client(), "id -u", check=False)
            if result.returncode == 0:
                break
            time.sleep(0.2)
        else:
            raise AssertionError(f"SSH login failed:\n{result.stderr}\n{compose('logs', '--no-color').stdout}")
        assert result.stdout.strip() == "1000", "SSH session is not dev"
        # A remote command runs over an SSH exec channel. An actual interactive
        # PTY login exercises a different sshd/audit path and was previously broken.
        interactive = client()
        interactive[-1:-1] = ["-tt"]
        commands = "\n".join([
            # Explicit failure branches preserve the interactive login shell's
            # logout behavior; 'set -e' can make Debian .bash_logout return 1.
            "test -t 0 && test -t 1 || exit 90",
            'printf "DCA_PTY_UID_%s_%s\\n" "$(id -u)" "$(tty)"',
            "tmux -L dockercat-review-pty new-session -d -s review || exit 91",
            "tmux -L dockercat-review-pty has-session -t review || exit 92",
            'printf "DCA_TMUX_%s\\n" "$(tmux -L dockercat-review-pty display-message -p -t review \u0027#S\u0027)"',
            "tmux -L dockercat-review-pty kill-server || true",
            'printf "DCA_PTY_DONE\\n"',
            "exit 0",
            "",
        ])
        pty = interactive_client(interactive, commands)
        assert pty.returncode == 0, (
            f"interactive PTY login rc={pty.returncode}: {pty.stdout}\n{pty.stderr}\n"
            f"sshd logs: {compose('logs', '--no-color').stdout}"
        )
        assert "DCA_PTY_UID_1000_/dev/pts/" in pty.stdout, (
            f"PTY login did not start as dev: {pty.stdout}"
        )
        assert "DCA_TMUX_review" in pty.stdout, "tmux failed in interactive SSH"
        assert "DCA_PTY_DONE" in pty.stdout, "interactive SSH did not complete the shell script"
        assert run(*client(wrong_key), "true", check=False).returncode != 0
        no_key = client()
        del no_key[3:5]
        no_key[-1:-1] = ["-o", "IdentityFile=none"]
        assert run(*no_key, "true", check=False).returncode != 0
        assert run(*client(user="root"), "true", check=False).returncode != 0
        password_client = client()
        password_client[-1:-1] = ["-o", "PreferredAuthentications=password,keyboard-interactive"]
        assert run(*password_client, "true", check=False).returncode != 0
        config = compose("exec", "-T", "agent", "/usr/sbin/sshd", "-T", "-f", "/run/sshd-dockercat.conf").stdout
        for policy in ("passwordauthentication no", "kbdinteractiveauthentication no", "permitrootlogin no",
                       "allowtcpforwarding local", "allowagentforwarding no", "allowstreamlocalforwarding no",
                       "gatewayports no", "permittunnel no", "permitopen localhost:8765 127.0.0.1:8765"):
            assert policy in config, f"effective SSH policy missing: {policy}"
        key_path = "/etc/ssh/dockercat-hostkeys/ssh_host_ed25519_key.pub"
        host_identity = compose("exec", "-T", "agent", "cat", key_path).stdout
        compose("up", "-d", "--no-build", "--force-recreate")
        assert compose("exec", "-T", "agent", "cat", key_path).stdout == host_identity
        # A missing public sidecar must be recovered from the same private key.
        compose("exec", "-T", "-u", "root", "agent", "rm", key_path)
        compose("up", "-d", "--no-build", "--force-recreate")
        assert compose("exec", "-T", "agent", "cat", key_path).stdout == host_identity
        # Exercise a real local callback-shaped connection without provider credentials.
        compose("exec", "-T", "-u", "dev", "agent", "sh", "-c", "printf callback-probe > /workspace/callback-probe")
        compose("exec", "-d", "-u", "dev", "agent", "python3", "-m", "http.server", "8765", "--bind", "127.0.0.1", "--directory", "/workspace")
        for destination, allowed in (("localhost:8765", True), ("localhost:8766", False)):
            local_port = free_port()
            command = client()
            command[-1:-1] = ["-N", "-L", f"127.0.0.1:{local_port}:{destination}"]
            with tempfile.TemporaryFile(mode="w+") as log:
                proc = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=log)
                try:
                    response = None
                    for attempt in range(30):
                        try:
                            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
                            with opener.open(f"http://127.0.0.1:{local_port}/callback-probe", timeout=1) as request:
                                response = request.read()
                            break
                        except (OSError, urllib.error.URLError):
                            if not allowed:
                                time.sleep(0.2)
                                log.seek(0)
                                if "administratively prohibited" in log.read():
                                    break
                            time.sleep(0.2)
                    if allowed:
                        assert response == b"callback-probe", "allowed callback forwarding failed"
                    else:
                        log.seek(0)
                        assert response is None and "administratively prohibited" in log.read()
                finally:
                    proc.terminate()
                    proc.wait(timeout=10)
        remote = client()
        remote[-1:-1] = ["-N", "-o", "ExitOnForwardFailure=yes", "-R", "0:localhost:8765"]
        result = run(*remote, check=False)
        assert result.returncode != 0 and "remote port forwarding failed" in result.stderr
        # Supply a real local agent so -A actually requests forwarding.
        # Keep the AF_UNIX address short even when checkout paths are long.
        agent_socket = Path("/tmp") / f"dca-agent-{uuid.uuid4().hex[:12]}.sock"
        with tempfile.TemporaryFile() as agent_log:
            agent = subprocess.Popen(["ssh-agent", "-D", "-a", str(agent_socket)], stdout=agent_log, stderr=agent_log)
            try:
                for attempt in range(30):
                    if agent_socket.exists():
                        break
                    time.sleep(0.1)
                agent_env = {**os.environ, "SSH_AUTH_SOCK": str(agent_socket)}
                run("ssh-add", str(key), env=agent_env)
                forwarded = client()
                forwarded[-1:-1] = ["-A"]
                run(*forwarded, 'test -z "${SSH_AUTH_SOCK:-}"', env=agent_env)
            finally:
                agent.terminate()
                agent.wait(timeout=10)
                agent_socket.unlink(missing_ok=True)
        print("PASS SSH: interactive PTY/tmux and command login as dev, auth denials, effective restrictions, host-key persistence, restricted synthetic callback and agent denial")


if __name__ == "__main__":
    baseline()
    with tempfile.TemporaryDirectory(prefix=".dockercat-fixtures-", dir=ROOT.parent) as path:
        directory = Path(path)
        directory.chmod(0o755)
        entrypoint_inputs(directory)
        vault_checks(directory)
        ssh_checks(directory)
    print("Runtime regressions passed; account OAuth, ARM64 hardware, VPN/mobile and Portainer acceptance remain manual")
