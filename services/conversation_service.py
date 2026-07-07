from database import SessionLocal
from models.identity import Identity


def get_or_create_identity(identity_id):

    db = SessionLocal()

    identity = (
        db.query(Identity)
        .filter(Identity.id == identity_id)
        .first()
    )

    if identity:
        return identity

    identity = Identity(
        id=identity_id,
        type="guest"
    )

    db.add(identity)
    db.commit()
    db.refresh(identity)

    return identity