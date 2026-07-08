from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from database import get_db
from models.user import User
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

    existing = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )


    if existing:
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


    return {
        "user_id": user.id,
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