.PHONY: help setup up down logs clean backend-install frontend-install

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: backend-install frontend-install ## Setup the complete project

up: ## Start all services via docker-compose
	docker-compose up -d

down: ## Stop all services via docker-compose
	docker-compose down

logs: ## Follow docker-compose logs
	docker-compose logs -f

clean: down ## Clean up containers and volumes
	docker-compose down -v --remove-orphans

backend-install: ## Install backend dependencies
	cd backend && poetry install

frontend-install: ## Install frontend dependencies
	cd frontend && npm install
