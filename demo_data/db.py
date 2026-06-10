from __future__ import annotations

import os
from collections.abc import Iterable
from decimal import Decimal

from demo_data.commerce import TableRows

DEFAULT_DATABASE_ENV = "DELPHI_DEMO_SOURCE_DATABASE_URL"


TABLE_COLUMNS: dict[str, list[str]] = {
    "sales.order_statuses": ["status_code", "status_name", "is_terminal"],
    "crm.customers": [
        "customer_id",
        "email",
        "segment",
        "region",
        "created_at",
        "updated_at",
    ],
    "catalog.products": [
        "product_id",
        "sku",
        "category",
        "list_price",
        "is_active",
        "snapshot_as_of",
    ],
    "sales.orders": [
        "order_id",
        "customer_id",
        "status_code",
        "ordered_at",
        "updated_at",
        "order_total",
    ],
    "sales.order_items": [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "created_at",
    ],
    "fulfillment.shipments": [
        "shipment_id",
        "order_id",
        "carrier",
        "shipped_at",
        "delivered_at",
    ],
}

PRIMARY_KEYS: dict[str, str] = {
    "sales.order_statuses": "status_code",
    "crm.customers": "customer_id",
    "catalog.products": "product_id",
    "sales.orders": "order_id",
    "sales.order_items": "order_item_id",
    "fulfillment.shipments": "shipment_id",
}


def database_url(value: str | None = None) -> str:
    resolved = value or os.getenv(DEFAULT_DATABASE_ENV)
    if not resolved:
        raise ValueError(f"Set {DEFAULT_DATABASE_ENV} or pass --database-url")
    return resolved


def apply_seed(url: str, tables: list[TableRows]) -> dict[str, int]:
    with _connect(url) as connection:
        with connection.cursor() as cursor:
            _create_schema(cursor)
            _truncate_all(cursor)
            for table in tables:
                _upsert_rows(cursor, table)
        connection.commit()
    return {table.table: len(table.rows) for table in tables}


def apply_incremental(url: str, tables: list[TableRows]) -> dict[str, int]:
    with _connect(url) as connection:
        with connection.cursor() as cursor:
            _create_schema(cursor)
            for table in tables:
                if table.table == "catalog.products":
                    cursor.execute("TRUNCATE TABLE catalog.products")
                _upsert_rows(cursor, table)
        connection.commit()
    return {table.table: len(table.rows) for table in tables}


def _connect(url: str):
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError(
            "psycopg is required to load demo data; run from the backend uv environment"
        ) from exc
    return psycopg.connect(url)


def _create_schema(cursor) -> None:
    statements = [
        "CREATE SCHEMA IF NOT EXISTS sales",
        "CREATE SCHEMA IF NOT EXISTS crm",
        "CREATE SCHEMA IF NOT EXISTS catalog",
        "CREATE SCHEMA IF NOT EXISTS fulfillment",
        """
        CREATE TABLE IF NOT EXISTS sales.order_statuses (
            status_code text PRIMARY KEY,
            status_name text NOT NULL,
            is_terminal boolean NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm.customers (
            customer_id text PRIMARY KEY,
            email text NOT NULL UNIQUE,
            segment text NOT NULL,
            region text NOT NULL,
            created_at timestamptz NOT NULL,
            updated_at timestamptz NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS catalog.products (
            product_id text PRIMARY KEY,
            sku text NOT NULL UNIQUE,
            category text NOT NULL,
            list_price numeric(12, 2) NOT NULL,
            is_active boolean NOT NULL,
            snapshot_as_of timestamptz NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sales.orders (
            order_id text PRIMARY KEY,
            customer_id text NOT NULL,
            status_code text NOT NULL REFERENCES sales.order_statuses(status_code),
            ordered_at timestamptz NOT NULL,
            updated_at timestamptz NOT NULL,
            order_total numeric(12, 2) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sales.order_items (
            order_item_id text PRIMARY KEY,
            order_id text NOT NULL REFERENCES sales.orders(order_id),
            product_id text NOT NULL,
            quantity integer NOT NULL,
            unit_price numeric(12, 2) NOT NULL,
            created_at timestamptz NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS fulfillment.shipments (
            shipment_id text PRIMARY KEY,
            order_id text NOT NULL REFERENCES sales.orders(order_id),
            carrier text NOT NULL,
            shipped_at timestamptz NOT NULL,
            delivered_at timestamptz
        )
        """,
    ]
    for statement in statements:
        cursor.execute(statement)


def _truncate_all(cursor) -> None:
    cursor.execute(
        """
        TRUNCATE TABLE
            fulfillment.shipments,
            sales.order_items,
            sales.orders,
            catalog.products,
            crm.customers,
            sales.order_statuses
        RESTART IDENTITY
        """
    )


def _upsert_rows(cursor, table: TableRows) -> None:
    if not table.rows:
        return
    columns = TABLE_COLUMNS[table.table]
    primary_key = PRIMARY_KEYS[table.table]
    placeholders = ", ".join(["%s"] * len(columns))
    assignments = ", ".join(
        f"{column} = EXCLUDED.{column}" for column in columns if column != primary_key
    )
    statement = (
        f"INSERT INTO {table.table} ({', '.join(columns)}) "
        f"VALUES ({placeholders}) "
        f"ON CONFLICT ({primary_key}) DO UPDATE SET {assignments}"
    )
    cursor.executemany(statement, [_row_values(row, columns) for row in table.rows])


def _row_values(row: dict[str, object], columns: Iterable[str]) -> tuple[object, ...]:
    values: list[object] = []
    for column in columns:
        value = row[column]
        if isinstance(value, Decimal):
            values.append(value)
        else:
            values.append(value)
    return tuple(values)
