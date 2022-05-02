FROM python:3.8-alpine
MAINTAINER tiger-park.com

ENV PYTHONUNBUFFERED 1

RUN apk add --update postgresql-client libjpeg-turbo
RUN apk add --no-cache --virtual .build-deps \
    gcc python3-dev postgresql-dev musl-dev zlib-dev jpeg-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN apk del --no-cache .build-deps

RUN mkdir /DJMAPS
WORKDIR /DJMAPS
COPY . /DJMAPS

RUN addgroup -g 994 jenkins
RUN adduser -D -u 997 jenkins -G jenkins
USER jenkins
