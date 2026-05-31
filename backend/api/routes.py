from fastapi import APIRouter
from services.expertise_service import get_experts

router = APIRouter()

@router.get("/experts/{system_name}")
def experts(system_name: str):
    return get_experts(system_name)