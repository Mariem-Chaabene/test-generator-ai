from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    email: str
    password: str
    guest_identity_id: Optional[int] = None


class LoginRequest(BaseModel):
    email: str
    password: str