FROM alpine:3.13
LABEL maintainer="Massimo Santini santini@di.unimi.it"
RUN apk add --no-cache --update python3 py3-pip; \
    pip3 install flask gunicorn
EXPOSE 8000
RUN mkdir -p /app/instance
COPY da /app/da
RUN chmod -R a+rX /app
WORKDIR /app
ENV FLASK_APP=da
CMD ["gunicorn", "--env", "SCRIPT_NAME=/da", "--bind=0.0.0.0:8080", "--workers", "4", "da:app"]
