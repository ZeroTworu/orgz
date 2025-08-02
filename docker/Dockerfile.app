FROM python:3.13 AS backend

RUN pip3 install poetry

WORKDIR /orgz
COPY ../migrations ./migrations

ADD ../poetry.lock ./poetry.lock
ADD ../pyproject.toml ./pyproject.toml
ADD ../alembic.ini ./alembic.ini

COPY ../app ./app

RUN poetry install --only main --no-root

ENV ALEMBIC_COMMAND="alembic upgrade head"
ENV UVICORN_COMMAND="uvicorn app.http.app:app --host 0.0.0.0"
CMD ["sh", "-c", "poetry run $ALEMBIC_COMMAND && poetry run $UVICORN_COMMAND"]
EXPOSE 8000
