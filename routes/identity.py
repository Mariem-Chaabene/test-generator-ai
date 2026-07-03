from fastapi import APIRouter

router = APIRouter()

@router.post("/identity")
def create_identity():
    return {"identity_id": 1}