FROM python:3.9.1-slim-buster

ARG pypi_host=pypi.tuna.tsinghua.edu.cn
ARG pypi_mirror=http://pypi.tuna.tsinghua.edu.cn/simple

ENV LC_ALL C.UTF-8

ENV LANG C.UTF-8

ENV PIP_INDEX_URL $pypi_mirror

ENV FLASK_ENV production

WORKDIR /app

RUN python -m pip install --upgrade pip --trusted-host ${pypi_host}

RUN pip install poetry --trusted-host ${pypi_host}

COPY poetry.lock poetry.lock

COPY pyproject.toml pyproject.toml

RUN poetry install --no-dev

COPY app app

COPY common common

COPY migrations migrations

COPY model model

COPY tasks tasks

COPY vendor vendor

COPY scripts scripts

COPY local_settings.py local_settings.py

COPY runner.py runner.py

RUN mkdir disk

RUN chmod a+x ./scripts/start_server.sh

EXPOSE 5000