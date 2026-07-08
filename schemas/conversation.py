from pydantic import BaseModel
from typing import List

from schemas.message import MessageResponse


class ConversationCreate(BaseModel):
    identity_id: int


class ConversationMessages(BaseModel):
    conversation_id: int
    messages: List[MessageResponse]