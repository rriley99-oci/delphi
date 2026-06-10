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

Run the same Alembic validation checks used by the migration CI:

```bash
uv run alembic history --verbose
uv run alembic heads --verbose
uv run alembic upgrade head --sql > /tmp/alembic-upgrade.sql
```

The Alembic CI workflow also applies `uv run alembic upgrade head` against a
temporary PostgreSQL service so migration lineage and upgrade execution are both
validated before merge.

Run Alembic commands from this `backend/` directory:

```bash
alembic current
alembic upgrade head
alembic revision --autogenerate -m "add dataset registry"
```

The migration chain now covers the current POC persistence slices for datasets,
contracts, evaluations, and violations.

## Podman Local Development

The repository root includes a Compose workflow for running the backend with a local PostgreSQL metadata database under Podman.

Start the stack from the repository root:

```bash
podman machine start
podman-compose up --build
```

If the Podman machine is already running, the `podman machine start` command is safe to re-run.

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
podman-compose down
```

Reset the local metadata database volume:

```bash
podman-compose down -v
```
