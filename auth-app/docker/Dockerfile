FROM alpine:3.10
LABEL maintainer="Massimo Santini santini@di.unimi.it"
RUN apk add --no-cache --update python3 py-gevent; \
    python3 -m pip install flask
EXPOSE 8000
RUN mkdir -p /app/da
COPY da /app/da
COPY run.py /app
WORKDIR /app
ENV FLASK_APP=da
CMD ["python3", "run.py"]
