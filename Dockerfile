FROM python:3.7-alpine3.9

COPY Pipfile /
COPY Pipfile.lock /

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    libpq \
    wkhtmltopdf \
    && pip3 install --no-cache-dir pipenv \
    && pipenv install --deploy --system \
    && apk del --no-cache .build-deps

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN chmod 755 /usr/src/app/docker-entrypoint.sh

CMD ["/usr/src/app/docker-entrypoint.sh"]
