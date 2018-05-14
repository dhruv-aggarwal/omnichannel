FROM python:2.7.15-alpine3.4

COPY . /www/app

WORKDIR /www/app

ENV UWSGI_INI /www/app/uwsgi.ini

RUN apk update
RUN apk add --update --no-cache libmysqlclient-dev

# Install dependencies
RUN pip install -r requirements.lock
