FROM debian:10.9
LABEL maintainer="Massimo Santini santini@di.unimi.it"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    openssh-client \
    python3-pip \
    rustc cargo python3-dev libssl-dev \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install docker[tls]

RUN groupadd -r cli \
    && useradd -m -r cli -g cli -s /bin/bash \
    && echo "cli ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd
USER cli

ENV SHELL=/bin/bash

RUN mkdir /home/cli/.ssh /home/cli/data && \
    ssh-keygen -qf /home/cli/.ssh/id_rsa -P '' -C 'danake_admin' && \
    chmod go= -R /home/cli

COPY --chown=cli ssh_config /home/cli/.ssh/config
COPY --chown=cli generate-cookies.py /home/cli/generate-cookies
COPY --chown=cli start-editor.py /home/cli/start-editor
COPY --chown=cli reaper-sign.py /home/cli/reaper-sign

WORKDIR /home/cli

ENV DANAKE_VERSION latest

ENTRYPOINT [ "python3" ]
