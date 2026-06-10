from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal

BASE_DATE = date(2026, 1, 1)


@dataclass(frozen=True)
class TableRows:
    table: str
    rows: list[dict[str, object]]


def parse_as_of(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def baseline_tables() -> list[TableRows]:
    customers = [
        _customer_row(i, BASE_DATE + timedelta(days=i % 45)) for i in range(1, 121)
    ]
    products = [_product_row(i, BASE_DATE + timedelta(days=90)) for i in range(1, 33)]
    orders, order_items, shipments = _order_window(BASE_DATE, 45)
    return [
        TableRows("sales.order_statuses", _order_statuses()),
        TableRows("crm.customers", customers),
        TableRows("catalog.products", products),
        TableRows("sales.orders", orders),
        TableRows("sales.order_items", order_items),
        TableRows("fulfillment.shipments", shipments),
    ]


def incremental_tables(as_of: datetime) -> list[TableRows]:
    as_of_date = as_of.date()
    day_index = max((as_of_date - BASE_DATE).days, 0)
    new_customers = [
        _customer_row(1000 + day_index * 3 + i, as_of_date) for i in range(1, 4)
    ]
    products = [_product_row(i, as_of_date) for i in range(1, 33)]
    orders, order_items, shipments = _order_window(as_of_date, 1)
    return [
        TableRows("sales.order_statuses", _order_statuses()),
        TableRows("crm.customers", new_customers),
        TableRows("catalog.products", products),
        TableRows("sales.orders", orders),
        TableRows("sales.order_items", order_items),
        TableRows("fulfillment.shipments", shipments),
    ]


def table_row_counts(tables: list[TableRows]) -> dict[str, int]:
    return {table.table: len(table.rows) for table in tables}


def _order_statuses() -> list[dict[str, object]]:
    return [
        {"status_code": "created", "status_name": "Created", "is_terminal": False},
        {"status_code": "paid", "status_name": "Paid", "is_terminal": False},
        {"status_code": "shipped", "status_name": "Shipped", "is_terminal": False},
        {"status_code": "delivered", "status_name": "Delivered", "is_terminal": True},
        {"status_code": "cancelled", "status_name": "Cancelled", "is_terminal": True},
    ]


def _customer_row(index: int, created_on: date) -> dict[str, object]:
    segments = ["consumer", "small_business", "enterprise"]
    regions = ["central", "northeast", "south", "west"]
    return {
        "customer_id": f"cust_{index:06d}",
        "email": f"customer{index:06d}@example.com",
        "segment": segments[index % len(segments)],
        "region": regions[index % len(regions)],
        "created_at": _at_noon(created_on),
        "updated_at": _at_noon(created_on + timedelta(days=index % 7)),
    }


def _product_row(index: int, as_of_date: date) -> dict[str, object]:
    categories = ["apparel", "home", "electronics", "outdoor"]
    price = Decimal("12.50") + Decimal(index * 3)
    return {
        "product_id": f"prod_{index:04d}",
        "sku": f"SKU-{index:04d}",
        "category": categories[index % len(categories)],
        "list_price": price,
        "is_active": index % 11 != 0,
        "snapshot_as_of": _at_noon(as_of_date),
    }


def _order_window(
    start_date: date, days: int
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    orders: list[dict[str, object]] = []
    order_items: list[dict[str, object]] = []
    shipments: list[dict[str, object]] = []
    for offset in range(days):
        order_date = start_date + timedelta(days=offset)
        day_number = (order_date - BASE_DATE).days
        for sequence in range(1, 7):
            order_id = f"ord_{day_number:05d}_{sequence:02d}"
            customer_index = ((day_number * 6 + sequence) % 120) + 1
            status = _status_for(day_number, sequence)
            orders.append(
                {
                    "order_id": order_id,
                    "customer_id": f"cust_{customer_index:06d}",
                    "status_code": status,
                    "ordered_at": _timestamp(order_date, 8 + sequence, sequence * 7),
                    "updated_at": _timestamp(order_date, 10 + sequence, sequence * 5),
                    "order_total": Decimal("35.00")
                    + Decimal(day_number + sequence * 9),
                }
            )
            for item_number in range(1, 3):
                quantity = (sequence + item_number) % 4 + 1
                product_index = ((day_number + sequence + item_number) % 32) + 1
                order_items.append(
                    {
                        "order_item_id": f"{order_id}_{item_number}",
                        "order_id": order_id,
                        "product_id": f"prod_{product_index:04d}",
                        "quantity": quantity,
                        "unit_price": Decimal("12.50") + Decimal(product_index * 3),
                        "created_at": _timestamp(
                            order_date, 8 + sequence, sequence * 7
                        ),
                    }
                )
            if status in {"shipped", "delivered"}:
                shipped_at = _timestamp(order_date + timedelta(days=1), 9, sequence)
                shipments.append(
                    {
                        "shipment_id": f"ship_{order_id}",
                        "order_id": order_id,
                        "carrier": ["ups", "fedex", "usps"][sequence % 3],
                        "shipped_at": shipped_at,
                        "delivered_at": (
                            shipped_at + timedelta(days=2)
                            if status == "delivered"
                            else None
                        ),
                    }
                )
    return orders, order_items, shipments


def _status_for(day_number: int, sequence: int) -> str:
    statuses = ["created", "paid", "shipped", "delivered", "cancelled"]
    return statuses[(day_number + sequence) % len(statuses)]


def _timestamp(value: date, hour: int, minute: int) -> datetime:
    return datetime.combine(value, time(hour % 24, minute % 60), tzinfo=UTC)


def _at_noon(value: date) -> datetime:
    return datetime.combine(value, time(12, 0), tzinfo=UTC)
