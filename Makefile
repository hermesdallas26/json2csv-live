
.PHONY: help install test lint format clean build

help:
	@echo "DevOrg CI/CD Commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make test     - Run tests with coverage"
	@echo "  make lint     - Run linting (ruff, black, mypy)"
	@echo "  make format   - Auto-format code"
	@echo "  make build    - Build wheel and sdist"
	@echo "  make clean    - Clean build artifacts"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/
	black --check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

build:
	python -m build

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
