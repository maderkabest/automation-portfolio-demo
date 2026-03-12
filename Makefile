.PHONY: install docker-up docker-down test-api test-ui test-hybrid test-integration test lint

## Install Python dependencies and Playwright browser
install:
	pip install -r requirements.txt && playwright install chromium

## Start PostgreSQL container in background
docker-up:
	docker compose -f docker/docker-compose.yml --env-file .env up -d

## Stop and remove PostgreSQL container
docker-down:
	docker compose -f docker/docker-compose.yml down

## Run API tests only
test-api:
	pytest tests/api/ -v

## Run UI tests only
test-ui:
	pytest tests/ui/ -v

## Run hybrid tests only (API setup + UI actions)
test-hybrid:
	pytest tests/hybrid/ -v

## Run database integration tests only
test-integration:
	pytest tests/integration/ -v

## Start Docker and run all test suites
test: docker-up
	pytest tests/api/ tests/ui/ tests/hybrid/ tests/integration/ -v

## Run Ruff linter and Mypy type checker
lint:
	ruff check src tests && mypy src
