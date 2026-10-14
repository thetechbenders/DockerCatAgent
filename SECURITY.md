# Security and vulnerability reporting

DockerCatAgent is pre-release. Do not place exploit details, credentials, private key material, OAuth callback URLs, or vault contents in public issues.

Use GitHub private vulnerability reporting if enabled, or reach a Techbenders maintainer privately through an established trusted channel. No security response-time guarantee has been established.

The baseline uses a non-root development user and no published ports, privileged mode, Docker socket or host network namespace. SSH opt-in has a different process privilege model: the SSH daemon may require root inside the container to authenticate and switch to the non-root dev user.

Docker does not prevent all malicious-code execution or exfiltration. Persistent volumes hold sensitive authentication state and must be backed up and protected accordingly. See [docs/security.md](docs/security.md).