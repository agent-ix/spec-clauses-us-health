.PHONY: test lint format build clean

test:
	pytest

lint:
	python -m compileall -q spec_clauses_us_health tests

format:
	python -m compileall -q spec_clauses_us_health tests

build:
	poetry build

clean:
	rm -rf build dist .pytest_cache .coverage
