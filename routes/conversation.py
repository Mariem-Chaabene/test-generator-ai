from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.conversation import Conversation
from schemas.conversation import ConversationCreate

@router.post("")
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db)
):

    conversation = Conversation(
        identity_id=request.identity_id
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id
    }