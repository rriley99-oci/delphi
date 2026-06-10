# Demo Source Data

This package creates a separate PostgreSQL source database for Delphi demos and
local contract evaluation. It is intentionally separate from the Delphi metadata
database used by the FastAPI backend.

## Datasets

The dataset definitions live under `demo_data/datasets/`, one YAML file per
source table:

- `sales.order_statuses`: static lookup table
- `crm.customers`: incremental dimension-style table
- `catalog.products`: snapshot table reloaded with kill-and-fill behavior
- `sales.orders`: incremental fact table
- `sales.order_items`: incremental child fact table
- `fulfillment.shipments`: incremental operational fact table

Each YAML file records the `database.schema.table` identity, load strategy, time
semantics, and generator hints that are useful when registering Delphi datasets
and authoring freshness, row-count, or custom SQL contracts.

## Database

Use a source database distinct from the Delphi metadata database. The loaders
read `DELPHI_DEMO_SOURCE_DATABASE_URL` unless `--database-url` is passed.

Example local URL:

```text
postgresql://delphi:delphi@localhost:5432/delphi_source
```

Create the source database if it does not exist, then run the loaders with the
backend environment so `psycopg` is available:

```bash
cd backend
PYTHONPATH=.. uv run python -m demo_data.seed --database-url postgresql://delphi:delphi@localhost:5432/delphi_source
PYTHONPATH=.. uv run python -m demo_data.incremental --as-of 2026-03-01T12:00:00Z --database-url postgresql://delphi:delphi@localhost:5432/delphi_source
```

When running from `backend/`, set `PYTHONPATH=..` if your shell does not already
include the repository root:

```bash
PYTHONPATH=.. uv run python -m demo_data.seed
```

## Load Behavior

The seed loader creates schemas and tables, truncates the demo source tables, and
loads deterministic historical data.

The incremental loader is keyed by `--as-of`. Running it repeatedly with the same
timestamp is idempotent:

- static lookup rows are upserted
- `catalog.products` is truncated and reloaded as the latest snapshot
- incremental tables use deterministic primary keys and upserts

This gives local demos repeatable data for freshness checks, row-count
thresholds, and cross-table custom SQL rules without coupling the source records
to Delphi's operational metadata tables.
