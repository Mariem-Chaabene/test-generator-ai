from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models.identity import Identity
from services.security import verify_token

security = HTTPBearer()


def get_current_identity(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = verify_token(token)

        identity = None


        # Cas Guest
        if payload.get("type") == "guest":

            identity = (
                db.query(Identity)
                .filter(
                    Identity.id == payload["identity_id"]
                )
                .first()
            )


        # Cas User
        elif "sub" in payload:

            user_id = int(payload["sub"])

            identity = (
                db.query(Identity)
                .filter(
                    Identity.user_id == user_id
                )
                .first()
            )


        if identity is None:
            raise HTTPException(
                status_code=401,
                detail="Identity not found"
            )


        return identity


    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )