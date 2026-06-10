from __future__ import annotations

import argparse

from demo_data.commerce import incremental_tables, parse_as_of
from demo_data.db import apply_incremental, database_url


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load deterministic incremental demo data"
    )
    parser.add_argument(
        "--as-of", required=True, help="UTC timestamp or date for the load"
    )
    parser.add_argument("--database-url", help="Postgres URL for the source database")
    args = parser.parse_args()

    as_of = parse_as_of(args.as_of)
    counts = apply_incremental(
        database_url(args.database_url), incremental_tables(as_of)
    )
    for table, count in counts.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
