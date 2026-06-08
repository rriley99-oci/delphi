from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_violations() -> dict[str, list[dict[str, str]]]:
    return {"items": []}


@router.patch("/{violation_id}")
async def update_violation(violation_id: str) -> dict[str, str]:
    return {"violation_id": violation_id, "status": "updated"}
