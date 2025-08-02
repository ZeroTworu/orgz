.PHONY: lint isort test infra app up

lint:
	poetry run flake8 app/

isort:
	poetry run isort app/ migrations/

test:
	ORGZ_PYTEST_ON=yes poetry run pytest

infra:
	docker-compose -f docker/docker-compose.infra.yaml up --remove-orphans

app:
	uvicorn  app.http.app:app --reload

up:
	docker-compose -f docker/docker-compose.app.yaml up --pull always --force-recreate
