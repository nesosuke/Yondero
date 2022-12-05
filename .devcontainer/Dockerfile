FROM python:3.10

COPY ./ /workspace
WORKDIR /workspace

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3-pip
RUN pip install --upgrade pip
RUN pip install poetry && poetry init -n
