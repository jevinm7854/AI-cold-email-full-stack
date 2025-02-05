# Makefile for local FastAPI development with PostgreSQL container

# Variables
COMPOSE_FILE = docker-compose.yml
DB_CONTAINER = postgres_container
DB_READY_TIMEOUT = 2
VENV_NAME = .venv
VENV_ACTIVATE = $(VENV_NAME)/bin/activate

# Default target
all: db-up start

# Start PostgreSQL container
db-up:
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep $(DB_READY_TIMEOUT)

# Stop PostgreSQL container
db-down:
	docker-compose -f $(COMPOSE_FILE) down

# Start FastAPI application locally
start:
	@echo "Activating virtual environment and starting FastAPI application..."
	@bash -c "source $(VENV_ACTIVATE) && fastapi dev main.py"

# View database logs
db-logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

# Help
help:
	@echo "Available targets:"
	@echo "  db-up    - Start PostgreSQL container"
	@echo "  db-down  - Stop PostgreSQL container"
	@echo "  start    - Start FastAPI application locally"
	@echo "  db-logs  - View database container logs"
	@echo "  all      - Start database and application (default)"

.PHONY: all db-up db-down start db-logs help