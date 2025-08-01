.PHONY: lint isort infra app up

lint:
	poetry run flake8 app/

isort:
	poetry run isort app/ migrations/

infra:
	docker-compose -f docker/docker-compose.infra.yaml up --remove-orphans

app:
	uvicorn  app.http.app:app --reload

up:
	docker-compose up --pull always --force-recreate
