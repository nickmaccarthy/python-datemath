
PYTHON ?= 3.14

.PHONY: sync test lint typecheck check build precommit-install precommit-run release-check docker-build docker-run test-build

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

precommit-install:
	uv run pre-commit install
	uv run pre-commit install --hook-type pre-push

precommit-run:
	uv run pre-commit run --all-files

release-check:
	uv run semantic-release -c .releaserc.toml version --print

docker-build:
	docker build -t python-datemath .

docker-run:
	docker run --rm python-datemath

test-build: docker-build docker-run
