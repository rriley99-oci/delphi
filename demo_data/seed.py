from __future__ import annotations

import argparse

from demo_data.commerce import baseline_tables
from demo_data.db import apply_seed, database_url


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed Delphi demo source Postgres data"
    )
    parser.add_argument("--database-url", help="Postgres URL for the source database")
    args = parser.parse_args()

    counts = apply_seed(database_url(args.database_url), baseline_tables())
    for table, count in counts.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
