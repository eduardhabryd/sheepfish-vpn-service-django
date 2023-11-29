FROM python:3.11.4-slim

LABEL maintainer = "eduardhabryd@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY . .

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install psycopg2

RUN pip install -r requirements.txt

RUN mkdir -p /vol/web/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    user

RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web/

USER user