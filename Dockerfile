FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml ./
RUN poetry install --no-root --without dev

COPY . .

EXPOSE 8083

ENTRYPOINT ["sh", "entrypoint.sh"]
