FROM debian:11

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    ca-certificates \
    curl \
    dumb-init \
    gdb \
    git \
    htop \
    less \
    locales \
    lsb-release \
    man \
    nano \
    openssh-server \
    pkg-config \
    procps \
    ssh \
    sudo \
    tar \
    vim \
    wget \
    python3 \
    python3-dev \
    python3-pip \
    python3-pylint-common \
    python3-setuptools \
    python3-wheel \
    openjdk-17-jdk-headless \
    openjdk-17-jre-headless \
    gradle \
    maven \
    && rm -rf /var/lib/apt/lists/*

# https://wiki.debian.org/Locale#Manually
RUN sed -i "s/# it_IT.UTF-8/it_IT.UTF-8/" /etc/locale.gen \
  && locale-gen
ENV LANG=it_IT.UTF-8

# shell
RUN chsh -s /bin/bash

# ssh-server
RUN mkdir -p /var/run/sshd && ssh-keygen -A
RUN echo 'Danake editor instance' > /etc/motd

# fixuid
RUN ARCH="$(dpkg --print-architecture)" && \
    curl -fsSL "https://github.com/boxboat/fixuid/releases/download/v0.5.1/fixuid-0.5.1-linux-$ARCH.tar.gz" | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

# code-server
ENV CODE_SERVER_VERSION=4.7.1
RUN cd tmp && curl -sLO https://github.com/coder/code-server/releases/download/v${CODE_SERVER_VERSION}/code-server_${CODE_SERVER_VERSION}_amd64.deb
RUN dpkg -i /tmp/code-server*.deb && rm /tmp/code-server*.deb

# extensions & configs
RUN adduser --gecos '' --disabled-password coder && \
  echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd
USER coder
ENV PATH "${PATH}:/home/coder/bin"
ENV SHELL /bin/bash
ENV VSCODE_EXTENSIONS "/home/coder/.local/share/code-server/extensions"
RUN rm -rf ${VSCODE_EXTENSIONS} && mkdir -p ${VSCODE_EXTENSIONS}
RUN bash -c 'for e in redhat.java vscjava.vscode-java-pack; do code-server --install-extension $e; done'
ENV VSCODE_USER "/home/coder/.local/share/code-server/User"
RUN rm -rf ${VSCODE_USER} && mkdir -p ${VSCODE_USER}
COPY --chown=coder:coder settings.json /home/coder/.local/share/code-server/User/

# ssh key
ARG authorized_keys
RUN mkdir -p /home/coder/.ssh/ && \
    echo ${authorized_keys} > /home/coder/.ssh/authorized_keys && \
    chmod go= -R /home/coder/.ssh

# go!
EXPOSE 8080
WORKDIR /home/coder
CMD ["bash", "-c", "/usr/bin/sudo /usr/sbin/sshd && exec code-server --disable-telemetry --bind-addr 0.0.0.0:8080 --auth none /home/coder"]