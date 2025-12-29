.PHONY: help build up down restart logs shell clean test

# Default target
help:
	@echo "Dagster Docker Compose Commands"
	@echo "================================"
	@echo ""
	@echo "  make build     - Build Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - Tail logs from all services"
	@echo "  make shell     - Open shell in code container"
	@echo "  make clean     - Remove containers, volumes, and images"
	@echo "  make reload    - Rebuild and restart code server only"
	@echo ""

# Build Docker images
build:
	docker compose build

# Start all services in background
up:
	docker compose up -d
	@echo ""
	@echo "✅ Dagster is starting..."
	@echo "📊 UI available at: http://localhost:3000"
	@echo ""
	@echo "Run 'make logs' to view logs"

# Start with build
up-build:
	docker compose up --build -d
	@echo ""
	@echo "✅ Dagster is starting..."
	@echo "📊 UI available at: http://localhost:3000"

# Stop all services
down:
	docker compose down

# Restart all services
restart:
	docker compose restart

# View logs
logs:
	docker compose logs -f

# Logs for specific services
logs-webserver:
	docker compose logs -f dagster_webserver

logs-daemon:
	docker compose logs -f dagster_daemon

logs-code:
	docker compose logs -f dagster_code

# Shell into code container
shell:
	docker compose exec dagster_code bash

# Rebuild and restart only the code server (for development)
reload:
	docker compose up --build -d dagster_code
	@echo ""
	@echo "✅ Code server reloaded"
	@echo "💡 Remember to reload the workspace in the UI (Deployment > Reload)"

# Clean everything
clean:
	docker compose down -v --rmi local
	@echo "✅ Cleaned up containers, volumes, and images"

# Check status
status:
	docker compose ps

# Run a one-off Python command
python:
	docker compose exec dagster_code python

# Validate dagster config
validate:
	docker compose exec dagster_code dagster instance info
