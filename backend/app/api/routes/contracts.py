from fastapi import APIRouter

router = APIRouter()


@router.get("/{contract_id}")
async def get_contract(contract_id: str) -> dict[str, str]:
    return {"contract_id": contract_id}
