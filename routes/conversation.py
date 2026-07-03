@router.post("/conversation")
def create_conversation(identity_id: int, db: Session = Depends(get_db)):

    conv = Conversation(
        identity_id=identity_id,
        title="New chat"
    )

    db.add(conv)
    db.commit()
    db.refresh(conv)

    return conv