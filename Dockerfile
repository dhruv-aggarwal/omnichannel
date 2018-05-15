FROM python:2.7.15-alpine3.4

COPY . /www/app

WORKDIR /www/app

ENV UWSGI_INI /www/app/uwsgi.ini

RUN apk --no-cache add --virtual build-dependencies \
      build-base \
      libfreetype6-dev \
      py-mysqldb \
      gcc \
      libc-dev \
      libffi-dev \
      mariadb-dev
RUN pip install -qq -r requirements.lock
RUN rm -rf .cache/pip && apk del build-dependencies

RUN apk -q --no-cache add mariadb-client-libs
# Install dependencies
#RUN pip install -r requirements.lock
