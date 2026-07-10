import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from jose import jwt, JWTError


SECRET_KEY = "secret-key-change-later"
ALGORITHM = "HS256"


def hash_password(password: str):

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed.decode("utf-8")



def verify_password(password: str, hashed_password: str):

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )



def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=60
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def create_guest_token(identity_id: int):
    payload = {
        "identity_id": identity_id,
        "type": "guest"
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )