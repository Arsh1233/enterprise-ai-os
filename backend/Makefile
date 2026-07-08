.PHONY: help setup install run test lint format typecheck docker-build docker-run clean

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: install ## Setup project

install: ## Install dependencies using uv
	uv pip install -e ".[dev]"

run: ## Run the FastAPI application locally
	uvicorn main:app --reload

test: ## Run tests
	pytest

lint: ## Run static analysis and linting
	ruff check .

format: ## Run code formatters
	ruff check . --fix
	black .

typecheck: ## Run type checking
	mypy .

docker-build: ## Build the Docker image
	docker build -t eaios-backend:latest .

docker-run: ## Run the Docker container
	docker run -p 8000:8000 eaios-backend:latest

clean: ## Clean generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
