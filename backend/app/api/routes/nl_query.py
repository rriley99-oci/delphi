from fastapi import APIRouter

router = APIRouter()


@router.post("/query")
async def query_metadata() -> dict[str, object]:
    return {"answer": "Not implemented", "evidence": []}
