.PHONY: test lint format build clean

test:
	pytest

lint:
	ruff check .
	black --check .
	python -m compileall -q spec_clauses_us_health tests

format:
	black .
	ruff check --fix .

build:
	poetry build

clean:
	rm -rf build dist .pytest_cache .coverage
