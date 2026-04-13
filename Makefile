
PYTHON ?= 3.14

.PHONY: sync test lint typecheck check build docker-build docker-run test-build

sync:
	uv sync --python $(PYTHON) --group dev

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy

check: lint typecheck test

build:
	uv build

docker-build:
	docker build -t python-datemath .

docker-run:
	docker run --rm python-datemath

test-build: docker-build docker-run
