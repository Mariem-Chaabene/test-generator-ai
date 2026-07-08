from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.identity import Identity
from models.conversation import Conversation

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

@router.get("/{identity_id}/conversations")
def get_conversations(
    identity_id: int,
    db: Session = Depends(get_db)
):

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.identity_id == identity_id
        )
        .order_by(
            Conversation.created_at.desc()
        )
        .all()
    )

    return {
        "identity_id": identity_id,
        "conversations": [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at
            }
            for conversation in conversations
        ]
    }