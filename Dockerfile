FROM docker.io/library/python:3.13

ARG PIPENV_VENV_IN_PROJECT=1
ARG USERNAME=ecomindai

ENV ECOMINDAI_SERVER_HOST=0.0.0.0
ENV ECOMINDAI_SERVER_PORT=8000

COPY . /app/

RUN useradd --create-home ${USERNAME} && \
    chown ${USERNAME}:${USERNAME} /app

USER ${USERNAME}
WORKDIR /app

RUN pip install pipenv --user && \
    ~/.local/bin/pipenv sync

EXPOSE ${ECOMINDAI_SERVER_PORT}

CMD ["./.venv/bin/python", "main.py"]
