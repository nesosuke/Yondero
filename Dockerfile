FROM python:3.8.13-slim

COPY . /app
WORKDIR /app

# update image and install curl
RUN apt-get update && apt-get install -y curl libpq-dev gcc

# install poetry 
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    . ~/.profile && \
    poetry install && \
    mkdir -p /app/logs

# remove unnecessary packages
RUN apt-get remove -y gcc curl && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD . ~/.profile && poetry run gunicorn api:api --config ./config/gunicorn.conf.py