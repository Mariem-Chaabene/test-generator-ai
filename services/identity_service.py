from models.identity import Identity


def get_or_create_guest(db):

    identity = Identity(
        type="guest"
    )

    db.add(identity)
    db.commit()
    db.refresh(identity)

    return identity