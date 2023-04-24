FROM python:3.8-slim-bullseye

RUN mkdir /code
WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip pipenv
#RUN pip install --upgrade pip flake8
COPY Pipfile* /code/
RUN pipenv install --system --ignore-pipfile

COPY . /code/

#RUN flake8 --ignore=E501,F401