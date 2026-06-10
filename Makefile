COMPOSE ?= podman-compose
BACKEND_DIR := backend
HEALTH_URL ?= http://localhost:8000/api/health
DEMO_SOURCE_URL ?= postgresql://delphi:delphi@localhost:5433/delphi_source
DEMO_AS_OF ?= 2026-03-01T12:00:00Z

.PHONY: up down logs reset-db health backend-check demo-seed demo-incremental

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

reset-db:
	$(COMPOSE) down -v

health:
	curl --fail --show-error --silent $(HEALTH_URL)

backend-check:
	cd $(BACKEND_DIR) && uv run black --check .
	cd $(BACKEND_DIR) && uv run ruff check .
	cd $(BACKEND_DIR) && uv run pytest tests

demo-seed:
	cd $(BACKEND_DIR) && PYTHONPATH=.. uv run python -m demo_data.seed --database-url $(DEMO_SOURCE_URL)

demo-incremental:
	cd $(BACKEND_DIR) && PYTHONPATH=.. uv run python -m demo_data.incremental --as-of $(DEMO_AS_OF) --database-url $(DEMO_SOURCE_URL)
