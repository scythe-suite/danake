FROM alpine:3.11
LABEL maintainer="Massimo Santini santini@di.unimi.it"
RUN apk add --no-cache --update python3; \
    python3 -m pip install flask gunicorn
EXPOSE 8000
ARG danake_gid
ARG danake_uid
USER ${danake_uid}:${danake_gid}
RUN mkdir -p /app/da
COPY da /app/da
COPY run.py /app
WORKDIR /app
ENV FLASK_APP=da
CMD ["gunicorn", "--env", "SCRIPT_NAME=/da", "--bind=0.0.0.0:8080", "--workers", "4", "da:app"]
