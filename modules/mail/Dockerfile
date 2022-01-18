FROM alpine:3.15
LABEL maintainer="Massimo Santini santini@di.unimi.it"
RUN apk add --no-cache --update python3 py3-pip; \
    pip3 install flask flask-mail gunicorn
EXPOSE 8000
RUN mkdir -p /app/instance
COPY mm /app/mm
RUN chmod -R a+rX /app
WORKDIR /app
ENV FLASK_APP=mm
CMD ["gunicorn", "--env", "SCRIPT_NAME=/mm", "--bind=0.0.0.0:8080", "--workers", "4", "mm:app"]
