FROM debian:10.9

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
    default-jdk-headless \
    default-jre-headless \
    gradle \
    maven \
    && rm -rf /var/lib/apt/lists/*

# https://wiki.debian.org/Locale#Manually
RUN sed -i "s/# it_IT.UTF-8/it_IT.UTF-8/" /etc/locale.gen \
  && locale-gen
ENV LANG=it_IT.UTF-8

RUN chsh -s /bin/bash

# ssh
RUN mkdir -p /var/run/sshd && ssh-keygen -A
RUN echo 'Danake editor instance' > /etc/motd

RUN ARCH="$(dpkg --print-architecture)" && \
    curl -fsSL "https://github.com/boxboat/fixuid/releases/download/v0.5/fixuid-0.5-linux-$ARCH.tar.gz" | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

RUN cd tmp && curl -sLO https://github.com/cdr/code-server/releases/download/v3.10.2/code-server_3.10.2_amd64.deb
RUN dpkg -i /tmp/code-server*$(dpkg --print-architecture).deb && rm /tmp/code-server*.deb

# Extensions & configs
RUN adduser --gecos '' --disabled-password coder && \
  echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd
USER coder
ENV PATH "${PATH}:/home/coder/bin"
ENV SHELL /bin/bash
ENV VSCODE_USER "/home/coder/.local/share/code-server/User"
ENV VSCODE_EXTENSIONS "/home/coder/.local/share/code-server/extensions"
RUN mkdir -p ${VSCODE_USER}
COPY --chown=coder:coder settings.json /home/coder/.local/share/code-server/User/
COPY --chown=coder:coder extensions.txt /tmp
RUN bash -c 'for e in $(cat /tmp/extensions.txt); do  code-server --install-extension $e; done' && rm -f /tmp/extensions.txt

# ssh
ARG authorized_keys
RUN mkdir -p /home/coder/.ssh/ && \
    echo ${authorized_keys} > /home/coder/.ssh/authorized_keys && \
    chmod go= -R /home/coder/.ssh

EXPOSE 8080
WORKDIR /home/coder
CMD ["bash", "-c", "/usr/bin/sudo /usr/sbin/sshd && exec code-server --disable-telemetry --bind-addr 0.0.0.0:8080 --auth none /home/coder"]