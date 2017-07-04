FROM node:6-alpine

WORKDIR /src
ADD . .

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    bash \
  && rm -rf /var/cache/apk/* \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

CMD [ "sh", "./start.sh" ]