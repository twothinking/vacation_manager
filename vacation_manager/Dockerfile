ARG BASEIMAGE=python:3.7.3-alpine3.9

FROM $BASEIMAGE as base
RUN apk add --no-cache \
    bash curl rsyslog rsyslog-tls tini \
    gcc libffi-dev linux-headers musl-dev openssl-dev tzdata
RUN pip install --upgrade pip==19.1.1 setuptools==41.0.1 wheel==0.33.1

WORKDIR /app
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

FROM base as dist
COPY --from=builder /install /usr/local
COPY . /app
WORKDIR /app
RUN pip install -e .
EXPOSE 80
CMD ["python", "vacation_manager.py"]
