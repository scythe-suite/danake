FROM debian:10
LABEL maintainer="Massimo Santini santini@di.unimi.it"
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install docker[tls]
COPY gencookies.py /cli/gencookies
COPY deploycs.py /cli/deploycs
WORKDIR /cli
ENTRYPOINT [ "python3" ]
CMD [ "gencookies" ]
