# Julep V2 Makefile
# AIDEV-NOTE: makefile-commands; common development tasks

.PHONY: help setup dev test lint clean generate typespec

help:
	@echo "Available commands:"
	@echo "  make setup    - Initial project setup"
	@echo "  make dev      - Start development environment"
	@echo "  make test     - Run test suite"
	@echo "  make lint     - Run linters"
	@echo "  make clean    - Clean generated files"
	@echo "  make generate - Generate code from TypeSpec"
	@echo "  make typespec - Compile TypeSpec definitions"

# AIDEV-NOTE: setup-command; install Python and Node.js dependencies
setup:
	poetry install
	npm install
	docker-compose pull
	@echo "Setup complete!"

# AIDEV-TODO: dev-command; start all services for development
dev:
	docker-compose up -d postgres
	poetry run python -m agents_api.api.main

# AIDEV-TODO: test-command; run pytest with coverage
test:
	poetry run pytest tests/ -v --cov=agents_api

# AIDEV-TODO: lint-command; run ruff and mypy
lint:
	poetry run ruff check .
	poetry run mypy agents_api/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/
	rm -rf generated/ node_modules/

# AIDEV-NOTE: typespec-commands; TypeSpec 1.1.0 code generation
typespec:
	npm run typespec:compile

generate: typespec
	@echo "Code generation complete!"
	@echo "Generated files in:"
	@echo "  - generated/openapi/    (OpenAPI 3.0 spec)"
	@echo "  - generated/json-schema/ (JSON Schema files)"