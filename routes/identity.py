from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.identity import Identity
from models.conversation import Conversation
from services.security import create_guest_token
from services.auth_service import get_current_identity

router = APIRouter(
    prefix="/identity",
    tags=["identity"]
)


@router.post("")
def create_identity(db: Session = Depends(get_db)):
    identity = Identity(
        type="guest"
    )
    db.add(identity)
    db.commit()
    db.refresh(identity)
    token = create_guest_token(identity.id)
    return {
        "guest_token": token
    }

@router.get("/conversations")
def get_conversations(
    current_identity: Identity = Depends(get_current_identity),
    db: Session = Depends(get_db)
):

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.identity_id == current_identity.id
        )
        .order_by(
            Conversation.created_at.desc()
        )
        .all()
    )

    return {
        "identity_id": current_identity.id,
        "conversations": [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at
            }
            for conversation in conversations
        ]
    }