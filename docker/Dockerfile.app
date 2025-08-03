FROM python:3.13.5-alpine3.22 AS builder

RUN pip install poetry

WORKDIR /orgz


COPY ../pyproject.toml ../poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-root

RUN find /usr/local/lib/python3.13/site-packages -name '*.pyc' -delete && \
    find /usr/local/lib/python3.13/site-packages -name '__pycache__' -delete

FROM alpine:3.22.1 AS runtime

RUN adduser app --disabled-password --no-create-home --uid 1337 --home /orgz

RUN rm -rf /usr/share/man /usr/share/doc /var/cache/apk/* /root/.cache

COPY --from=builder /usr/local/lib/ /usr/local/lib/
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
