from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.identity import Identity

router = APIRouter(
    prefix="/identity",
    tags=["identity"]
)


@router.post("")
def create_identity(db: Session = Depends(get_db)):
    identity = Identity(type="guest")

    db.add(identity)
    db.commit()
    db.refresh(identity)

    return {
        "identity_id": identity.id
    }