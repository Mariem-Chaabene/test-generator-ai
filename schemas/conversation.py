from pydantic import BaseModel
from typing import List

from schemas.message import MessageResponse

class ConversationMessages(BaseModel):
    conversation_id: int
    messages: List[MessageResponse]