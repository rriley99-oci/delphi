from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def trigger_evaluation() -> dict[str, str]:
    return {"status": "queued"}


@router.get("/{evaluation_id}")
async def get_evaluation(evaluation_id: str) -> dict[str, str]:
    return {"evaluation_id": evaluation_id}
