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
python -m pip install -e ".[dev]"
```

Run Alembic commands from this `backend/` directory:

```bash
alembic current
alembic upgrade head
alembic revision --autogenerate -m "add dataset registry"
```

The initial migration intentionally creates no product tables. It verifies migration wiring while keeping dataset, contract, evaluation, and violation schemas for their own vertical slices.
