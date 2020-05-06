FROM debian:10

ENV DEBIAN_FRONTEND noninteractive

# Packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    gpg \
    curl \
    wget \
    lsb-release \
    ca-certificates \
    dumb-init \
    gpg-agent \
    apt-utils \
    locales \
    man \
    git \
    sudo \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Common SDK
RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    sudo \
    gdb \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Node 10.x SDK
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Golang 1.13 SDK
RUN curl -sL https://dl.google.com/go/go1.13.linux-amd64.tar.gz | tar -zx -C /usr/local

# Python SDK
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-pylint-common \
    && rm -rf /var/lib/apt/lists/*

# Java SDK
RUN apt-get update && apt-get install --no-install-recommends -y \
    default-jre-headless \
    default-jdk-headless \
    maven \
    gradle \
    && rm -rf /var/lib/apt/lists/*

# Code-Server
RUN apt-get update && apt-get install --no-install-recommends -y \
    tar \
    openssl \
    locales \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
ENV DISABLE_TELEMETRY true

ENV CODE_VERSION="3.2.0"
RUN curl -sL https://github.com/cdr/code-server/releases/download/${CODE_VERSION}/code-server-${CODE_VERSION}-linux-x86_64.tar.gz | tar --strip-components=1 -zx -C /usr/local/bin

# Setup User
RUN groupadd -r coder \
    && useradd -m -r coder -g coder -s /bin/bash \
    && echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd
USER coder
ENV SHELL=/bin/bash

# Setup User Go Environment
ENV PATH "${PATH}:/usr/local/go/bin:/home/coder/go/bin"

# Setup User Visual Studio Code Extentions
ENV VSCODE_USER "/home/coder/.local/share/code-server/User"
ENV VSCODE_EXTENSIONS "/home/coder/.local/share/code-server/extensions"

# Extensions
COPY --chown=coder:coder extensions.txt /tmp
RUN bash -c 'for e in $(cat /tmp/extensions.txt); do  code-server --install-extension $e; done' && rm -f /tmp/extensions.txt

# Setup User Workspace
RUN mkdir -p ${VSCODE_USER}
COPY --chown=coder:coder settings.json /home/coder/.local/share/code-server/User/
RUN mkdir -p /home/coder/project
WORKDIR /home/coder/project

EXPOSE 8080

ENTRYPOINT ["dumb-init", "--"]
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "none", "/home/coder/project"]