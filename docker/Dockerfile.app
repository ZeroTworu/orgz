FROM python:3.13.5-alpine3.22 AS builder

RUN pip install poetry

WORKDIR /orgz


COPY ../pyproject.toml ../poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-root

FROM python:3.13.5-alpine3.22 AS runtime

RUN adduser app --disabled-password --no-create-home --uid 1337 --home /orgz

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

USER app

WORKDIR /orgz
COPY ../app ./app
COPY ../migrations ./migrations
COPY ../alembic.ini .
COPY ../pyproject.toml .
COPY ../poetry.lock .


ENV ALEMBIC_COMMAND="alembic upgrade head"
ENV UVICORN_COMMAND="uvicorn app.http.app:app --host 0.0.0.0"

CMD ["sh", "-c", "$ALEMBIC_COMMAND && $UVICORN_COMMAND"]
EXPOSE 8000
