# Backend

This directory contains the Delphi FastAPI backend.

The initial scaffold is organized as a modular monolith with clear domain boundaries:

- datasets
- contracts
- evaluations
- violations
- natural language query

Future iterations can extract these modules into separate services if scaling or team boundaries justify it.

## Local Database

Delphi is Postgres-first. The backend reads its metadata database connection from `DELPHI_DATABASE_URL` or `DATABASE_URL`.

Default local value:

```text
postgresql+psycopg://delphi:delphi@localhost:5432/delphi
```

Install backend dependencies for local development:

```bash
uv sync --extra dev
```

Run the same backend quality checks used by CI:

```bash
uv run black --check .
uv run ruff check .
uv run pytest tests
```

Run Alembic commands from this `backend/` directory:

```bash
alembic current
alembic upgrade head
alembic revision --autogenerate -m "add dataset registry"
```

The initial migration intentionally creates no product tables. It verifies migration wiring while keeping dataset, contract, evaluation, and violation schemas for their own vertical slices.

## Docker Local Development

The repository root includes a Docker Compose workflow for running the backend with a local PostgreSQL metadata database.

Start the stack from the repository root:

```bash
docker compose up --build
```

If your local Docker installation uses the legacy Compose command, run `docker-compose up --build` instead.

The backend is available at:

```text
http://localhost:8000/api/health
```

Compose sets the backend database URL to:

```text
postgresql+psycopg://delphi:delphi@postgres:5432/delphi
```

The backend container runs `alembic upgrade head` before starting Uvicorn, so local schema changes are applied when the stack starts.

Stop the stack:

```bash
docker compose down
```

Legacy Compose equivalent: `docker-compose down`.

Reset the local metadata database volume:

```bash
docker compose down -v
```

Legacy Compose equivalent: `docker-compose down -v`.
