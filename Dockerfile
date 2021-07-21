FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction 

COPY / /code/