FROM debian:10
LABEL maintainer="Massimo Santini santini@di.unimi.it"
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install docker[tls]
RUN mkdir /cli && chmod a+rx /cli
COPY generate-cookies.py /cli/generate-cookies
COPY start-editor.py /cli/start-editor
RUN chmod a+r /cli/*
WORKDIR /cli
ENV DANAKE_VERSION latest
ENTRYPOINT [ "python3" ]
