from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.identity import Identity

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/identity")
def get_identity(db: Session = Depends(get_db)):
    identity = Identity(type="guest")
    db.add(identity)
    db.commit()
    db.refresh(identity)

    return {"identity_id": identity.id}