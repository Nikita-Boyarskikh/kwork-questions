FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache --virtual build-deps libffi-dev g++ zlib-dev freetype-dev jpeg-dev postgresql-dev \
    && apk add --no-cache libjpeg libpq freetype \
    && pip install pipenv

COPY ./Pipfile ./Pipfile.lock ./

RUN pipenv install --system && apk del --purge build-deps

WORKDIR /usr/src/app
COPY . .

ENTRYPOINT ["./entrypoint.sh"]
