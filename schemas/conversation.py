from pydantic import BaseModel

class ConversationCreate(BaseModel):
    identity_id: int