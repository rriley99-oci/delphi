from fastapi import APIRouter

from app.api.routes import (
    contracts,
    datasets,
    debug,
    evaluations,
    health,
    nl_query,
    violations,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
api_router.include_router(
    evaluations.router, prefix="/evaluations", tags=["evaluations"]
)
api_router.include_router(violations.router, prefix="/violations", tags=["violations"])
api_router.include_router(nl_query.router, prefix="/nl", tags=["natural-language"])
