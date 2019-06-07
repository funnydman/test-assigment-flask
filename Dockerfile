FROM python:3.7-alpine3.9

RUN pip3 install --no-cache-dir pipenv
RUN apk add libpq wkhtmltopdf

COPY Pipfile /
COPY Pipfile.lock /

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && set -ex && pipenv install --deploy --system \
    && apk del --no-cache .build-deps

COPY . /usr/src/app
WORKDIR /usr/src/app

USER 1000:1000

CMD ["flask", "run", "--host=0.0.0.0"]
