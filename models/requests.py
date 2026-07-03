from pydantic import BaseModel

class CodeRequest(BaseModel):
    code: str
    identity_id: str