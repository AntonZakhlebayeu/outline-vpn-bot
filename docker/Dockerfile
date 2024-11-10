FROM python:3.11-slim

ENV POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -


ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . /app

RUN poetry install --no-root

CMD ["python", "main.py"]
