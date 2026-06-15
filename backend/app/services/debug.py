from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.debug import DebugSQLResponse


def execute_debug_sql(db: Session, query: str) -> DebugSQLResponse:
    statement = text(query)

    try:
        result = db.execute(statement)
        columns: list[str] = []
        rows: list[dict[str, object]] = []

        if result.returns_rows:
            columns = list(result.keys())
            rows = [dict(row) for row in result.mappings().all()]
            row_count = len(rows)
        else:
            row_count = max(result.rowcount, 0)

        db.commit()
    except Exception:
        db.rollback()
        raise

    return DebugSQLResponse(
        query=query,
        row_count=row_count,
        columns=columns,
        rows=rows,
        committed=True,
    )
