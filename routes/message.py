@router.post("/message")
def send_message(conversation_id: int, content: str, db: Session = Depends(get_db)):

    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=content
    )

    db.add(user_msg)

    # 🔥 CALL TON IA ICI
    ai_response = "generated answer here"

    bot_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response
    )

    db.add(bot_msg)
    db.commit()

    return {
        "response": ai_response
    }