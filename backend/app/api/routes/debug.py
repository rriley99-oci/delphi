from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.schemas.debug import DebugSQLRequest, DebugSQLResponse
from app.services.debug import execute_debug_sql

router = APIRouter()


@router.post("/sql", response_model=DebugSQLResponse)
def run_debug_sql(
    request: DebugSQLRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> DebugSQLResponse:
    if not settings.debug_sql_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Debug SQL endpoint is disabled.",
        )

    try:
        return execute_debug_sql(db, request.query)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
