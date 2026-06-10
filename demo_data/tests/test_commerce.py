from __future__ import annotations

from pathlib import Path

from demo_data.commerce import baseline_tables, incremental_tables, parse_as_of

EXPECTED_DATASETS = {
    "order_statuses.yaml",
    "customers.yaml",
    "products.yaml",
    "orders.yaml",
    "order_items.yaml",
    "shipments.yaml",
}


def test_one_yaml_definition_per_demo_dataset() -> None:
    dataset_dir = Path(__file__).resolve().parents[1] / "datasets"
    names = {path.name for path in dataset_dir.glob("*.yaml")}
    assert names == EXPECTED_DATASETS
    for path in dataset_dir.glob("*.yaml"):
        body = path.read_text()
        assert "identity:" in body
        assert "load_strategy:" in body
        assert "time_semantics:" in body
        assert "generator_hints:" in body


def test_baseline_generation_covers_required_source_tables() -> None:
    tables = {table.table: table.rows for table in baseline_tables()}
    assert set(tables) == {
        "sales.order_statuses",
        "crm.customers",
        "catalog.products",
        "sales.orders",
        "sales.order_items",
        "fulfillment.shipments",
    }
    assert len(tables["sales.order_statuses"]) == 5
    assert len(tables["crm.customers"]) == 120
    assert len(tables["catalog.products"]) == 32
    assert len(tables["sales.orders"]) == 270
    assert len(tables["sales.order_items"]) == 540
    assert len(tables["fulfillment.shipments"]) > 0


def test_incremental_generation_is_deterministic_for_same_as_of() -> None:
    as_of = parse_as_of("2026-03-01T12:00:00Z")
    first = incremental_tables(as_of)
    second = incremental_tables(as_of)
    assert first == second


def test_incremental_generation_changes_keys_for_different_as_of() -> None:
    first = {
        table.table: table.rows
        for table in incremental_tables(parse_as_of("2026-03-01T12:00:00Z"))
    }
    second = {
        table.table: table.rows
        for table in incremental_tables(parse_as_of("2026-03-02T12:00:00Z"))
    }
    assert first["sales.orders"][0]["order_id"] != second["sales.orders"][0]["order_id"]
    assert (
        first["catalog.products"][0]["product_id"]
        == second["catalog.products"][0]["product_id"]
    )
