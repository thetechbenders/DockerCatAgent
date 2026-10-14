# syntax=docker/dockerfile:1
FROM debian:bookworm-slim
ARG DEBIAN_FRONTEND=noninteractive
ARG CLAUDE_CHANNEL=stable

RUN --mount=type=secret,id=proxy_ca,target=/run/secrets/proxy_ca,mode=0444,required=false \
    set -eux; \
    # Keep installed tool manpages so Debian alternatives have valid slave links. \
    sed -i '\|^path-exclude /usr/share/man/\*|d' /etc/dpkg/dpkg.cfg.d/docker; \
    apt_ca=''; \
    if [ -f /run/secrets/proxy_ca ]; then apt_ca='-oAcquire::https::CaInfo=/run/secrets/proxy_ca'; fi; \
    apt-get $apt_ca update; \
    apt-get $apt_ca install -y --no-install-recommends \
      bash ca-certificates curl gnupg git openssh-client openssh-server \
      tmux jq less ripgrep vim-tiny nano procps psmisc \
      build-essential make pkg-config python3 python3-venv python3-pip \
      unzip zip tar xz-utils file tini; \
    rm -rf /var/lib/apt/lists/*; \
    rm -f /etc/ssh/ssh_host_*

# Verify Anthropic's published signing key before using its Debian repository.
RUN --mount=type=secret,id=proxy_ca,target=/run/secrets/proxy_ca,mode=0444,required=false \
    set -eux; \
    apt_ca=''; \
    if [ -f /run/secrets/proxy_ca ]; then \
      export CURL_CA_BUNDLE=/run/secrets/proxy_ca; \
      apt_ca='-oAcquire::https::CaInfo=/run/secrets/proxy_ca'; \
    fi; \
    case "$CLAUDE_CHANNEL" in stable|latest) ;; *) exit 2 ;; esac; \
    install -d -m 0755 /etc/apt/keyrings; \
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
      -o /etc/apt/keyrings/claude-code.asc; \
    actual="$(gpg --batch --show-keys --with-colons /etc/apt/keyrings/claude-code.asc | awk -F: '$1 == "fpr" { print $10; exit }')"; \
    test "$actual" = "31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE"; \
    printf 'deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/%s %s main\n' \
      "$CLAUDE_CHANNEL" "$CLAUDE_CHANNEL" > /etc/apt/sources.list.d/claude-code.list; \
    apt-get $apt_ca update; \
    apt-get $apt_ca install -y --no-install-recommends claude-code; \
    rm -rf /var/lib/apt/lists/*; \
    claude --version

RUN set -eux; \
    groupadd --gid 1000 dev; \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash dev; \
    passwd -d dev; \
    install -d -o dev -g dev -m 0755 /workspace; \
    install -d -o dev -g dev -m 0700 /home/dev/.ssh /home/dev/.claude; \
    install -d -m 0700 /etc/ssh/dockercat-hostkeys; \
    install -d -m 0755 /run/sshd

COPY scripts/entrypoint.sh /usr/local/bin/dockercat-entrypoint
COPY scripts/healthcheck.sh /usr/local/bin/dockercat-healthcheck
COPY scripts/smoke.sh /usr/local/bin/dockercat-smoke
COPY config/sshd_config.template /etc/ssh/sshd_config.dockercat.template
RUN chmod 0755 /usr/local/bin/dockercat-entrypoint /usr/local/bin/dockercat-healthcheck /usr/local/bin/dockercat-smoke

ENV HOME=/home/dev TERM=xterm-256color
WORKDIR /workspace
USER dev
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/dockercat-entrypoint"]
CMD ["sleep", "infinity"]
