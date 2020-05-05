FROM debian:10
LABEL maintainer="Massimo Santini santini@di.unimi.it"
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install docker[tls]
COPY generate-cookies.py /cli/generate-cookies
COPY start-editor.py /cli/start-editor
WORKDIR /cli
ARG danake_uid
ARG danake_gid
USER ${danake_uid}:${danake_gid}
ENV DANAKE_VERSION latest
ENTRYPOINT [ "python3" ]
