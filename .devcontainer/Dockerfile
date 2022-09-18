FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

ARG USERNAME=vscode
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install --no-install-recommends python3-pip
RUN pip3 install poetry

WORKDIR /workspace
RUN touch .bash_history && chown ${USERNAME} .bash_history
