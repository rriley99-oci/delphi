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

## Container Local Development

The repository root includes a Compose workflow for running the backend with a
local PostgreSQL metadata database and a separate demo source PostgreSQL
database.

On macOS with Podman, start the VM first:

```bash
podman machine start
```

If Podman reports that the system helper service is not installed, either
export the `DOCKER_HOST` value printed by `podman machine start` in the same
terminal session or use `podman-compose`, which talks to Podman directly.

Start the stack from the repository root:

```bash
podman-compose up --build
```

Docker Compose also works when Docker is your active runtime:

```bash
docker compose up --build
```

Common commands are available through the root `Makefile`:

```bash
make up
make logs
make down
make reset-db
```

The backend is available at:

```text
http://localhost:8000/api/health
```

Check it from another terminal:

```bash
curl --fail http://localhost:8000/api/health
```

Compose sets the backend database URL to:

```text
postgresql+psycopg://delphi:delphi@postgres:5432/delphi
```

The demo source database is available from the host at:

```text
postgresql://delphi:delphi@localhost:5433/delphi_source
```

The backend container runs `alembic upgrade head` before starting Uvicorn, so local schema changes are applied when the stack starts.

Stop the stack:

```bash
podman-compose down
```

Docker Compose equivalent: `docker compose down`.

Reset the local metadata and demo source database volumes:

```bash
podman-compose down -v
```

Docker Compose equivalent: `docker compose down -v`.
