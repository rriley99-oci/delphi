from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_datasets() -> dict[str, list[dict[str, str]]]:
    return {"items": []}


@router.get("/{dataset_id}")
async def get_dataset(dataset_id: str) -> dict[str, str]:
    return {"dataset_id": dataset_id}
