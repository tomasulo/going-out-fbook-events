FROM node:6-alpine

COPY /node_modules /node_modules

COPY /scripts /scripts
CMD [ "sh", "/scripts/start.sh" ]

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    bash \
  && rm -rf /var/cache/apk/*

COPY requirements.txt /tmp/
RUN pip install --upgrade pip \
      && pip install --no-cache-dir -r /tmp/requirements.txt


