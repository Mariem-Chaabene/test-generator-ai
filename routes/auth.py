from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth_service import get_current_identity
from database import get_db
from models.user import User
from models.identity import Identity

from schemas.auth import (
    RegisterRequest,
    LoginRequest
)

from services.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)



@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    user = User(
        email=request.email,
        password=hash_password(
            request.password
        )
    )


    db.add(user)
    db.commit()
    db.refresh(user)


     # CAS 1 : le guest existe déjà
    if request.guest_identity_id:

        identity = (
            db.query(Identity)
            .filter(
                Identity.id == request.guest_identity_id
            )
            .first()
        )


        if identity is None:
            raise HTTPException(
                status_code=404,
                detail="Guest identity not found"
            )


        # Transformation guest -> user
        identity.user_id = user.id
        identity.type = "user"


    # CAS 2 : création compte directement
    else:

        identity = Identity(
            user_id=user.id,
            type="user"
        )

        db.add(identity)


    db.commit()
    db.refresh(identity)


    return {
        "user_id": user.id,
        "identity_id": identity.id,
        "email": user.email
    }



@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    if not verify_password(
        request.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_identity: Identity = Depends(get_current_identity)
):

    if current_identity.type == "guest":

        return {
            "type": "guest",
            "identity_id": current_identity.id,
            "user": None
        }


    return {
        "type": "user",
        "identity_id": current_identity.id,
        "user": {
            "id": current_identity.user.id,
            "email": current_identity.user.email
        }
    }
	
@router.get("/me")
def get_me(
    current_identity: Identity = Depends(get_current_identity)
):

    if current_identity.type == "guest":

        return {
            "type": "guest",
            "identity_id": current_identity.id,
            "user": None
        }


    return {
        "type": "user",
        "identity_id": current_identity.id,
        "user": {
            "id": current_identity.user.id,
            "email": current_identity.user.email
        }
    }