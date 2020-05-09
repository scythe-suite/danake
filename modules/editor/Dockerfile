FROM debian:10

ENV DEBIAN_FRONTEND noninteractive

# Packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    apt-utils \
    ca-certificates \
    curl \
    dumb-init \
    git \
    gpg \
    gpg-agent \
    less \
    locales \
    lsb-release \
    man \
    openssh-server \
    sudo \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Common SDK
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    gdb \
    git \
    pkg-config \
    sudo \
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
    python3-pylint-common \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Java SDK
RUN apt-get update && apt-get install --no-install-recommends -y \
    default-jdk-headless \
    default-jre-headless \
    gradle \
    maven \
    && rm -rf /var/lib/apt/lists/*

# Code-Server
RUN apt-get update && apt-get install --no-install-recommends -y \
    locales \
    net-tools \
    openssl \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Miscellany setup
RUN localedef -i it_IT -c -f UTF-8 -A /usr/share/locale/locale.alias it_IT.UTF-8
ENV LANG it_IT.UTF-8
RUN echo 'Danake editor instance' > /etc/motd

# Install code serer
ENV CODE_VERSION="3.2.0"
RUN curl -sL https://github.com/cdr/code-server/releases/download/${CODE_VERSION}/code-server-${CODE_VERSION}-linux-x86_64.tar.gz | tar --strip-components=1 -zx -C /usr/local/bin

# Setup User
RUN mkdir -p /var/run/sshd && ssh-keygen -A
RUN groupadd -r coder \
    && useradd -m -r coder -g coder -s /bin/bash \
    && echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd
USER coder
ENV SHELL=/bin/bash

# Setup User Go Environment
ENV PATH "${PATH}:/home/coder/bin:/usr/local/go/bin:/home/coder/go/bin"

# Setup User Visual Studio Code Extentions
ENV VSCODE_USER "/home/coder/.local/share/code-server/User"
ENV VSCODE_EXTENSIONS "/home/coder/.local/share/code-server/extensions"

# Extensions
COPY --chown=coder:coder extensions.txt /tmp
RUN bash -c 'for e in $(cat /tmp/extensions.txt); do  code-server --install-extension $e; done' && rm -f /tmp/extensions.txt

# Setup User Workspace
RUN mkdir -p ${VSCODE_USER} && mkdir -p /home/coder/.ssh
COPY --chown=coder:coder settings.json /home/coder/.local/share/code-server/User/
WORKDIR /home/coder/

# Add authorized_keys
ARG authorized_keys
RUN mkdir -p /home/coder/.ssh/ && \
    echo ${authorized_keys} > /home/coder/.ssh/authorized_keys && \
    chmod go= -R /home/coder/.ssh

EXPOSE 8080

ENTRYPOINT ["dumb-init", "--"]
# https://github.com/Yelp/dumb-init#using-a-shell-for-pre-start-hooks
CMD ["bash", "-c", "/usr/bin/sudo /usr/sbin/sshd && exec code-server --disable-telemetry --disable-updates --bind-addr 0.0.0.0:8080 --auth none /home/coder"]