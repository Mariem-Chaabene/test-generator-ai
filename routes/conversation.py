from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from services.auth_service import get_current_identity
from models.identity import Identity
from database import get_db
from models.conversation import Conversation
# from schemas.conversation import ConversationCreate
from models.requests import CodeRequest
from services.ai_service import generate_tests
from models.message import Message
from schemas.conversation import ConversationMessages

router = APIRouter(
    prefix="/conversation",
    tags=["conversation"]
)

@router.post("")
def create_conversation(
    current_identity: Identity = Depends(get_current_identity),
    db: Session = Depends(get_db)
):

    conversation = Conversation(
        identity_id=current_identity.id,
        title="New chat"
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id
    }

@router.post("/{id}/generate-tests")
def generate(
    id: int,
    request: CodeRequest,
    current_identity: Identity = Depends(get_current_identity),
    db: Session = Depends(get_db)
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == id,
            Conversation.identity_id == current_identity.id
        )
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # 1 - Enregistrer le message utilisateur
    user_message = Message(
        conversation_id=id,
        role="user",
        content=request.code
    )

    db.add(user_message)
    db.commit()

    # 2 - Appeler Ollama
    tests = generate_tests(request.code)

    # 3 - Enregistrer la réponse IA
    assistant_message = Message(
        conversation_id=id,
        role="assistant",
        content=tests
    )

    db.add(assistant_message)
    db.commit()

    # 4 - Retourner le résultat
    return {
        "conversation_id": id,
        "tests": tests
    }


@router.post("/{id}/upload-java")
async def upload_java(
    id: int,
    file: UploadFile = File(...),
	current_identity: Identity = Depends(get_current_identity),
    db: Session = Depends(get_db)
):
	conversation = (
		db.query(Conversation)
		.filter(
			Conversation.id == id,
			Conversation.identity_id == current_identity.id
		)
		.first()
	)

	if conversation is None:
		raise HTTPException(
			status_code=404,
			detail="Conversation not found"
		)
		# 1 - Lire le fichier Java

		content = await file.read()

		java_code = content.decode("utf-8")


		# 2 - Enregistrer le message utilisateur

		user_message = Message(
			conversation_id=id,
			role="user",
			content=java_code
		)

		db.add(user_message)
		db.commit()


		# 3 - Appeler Ollama

		tests = generate_tests(java_code)


		# 4 - Enregistrer la réponse IA

		assistant_message = Message(
			conversation_id=id,
			role="assistant",
			content=tests
		)

		db.add(assistant_message)
		db.commit()


		# 5 - Retourner le résultat

		return {
			"conversation_id": id,
			"filename": file.filename,
			"tests": tests
		}

@router.get("/{id}/messages", response_model=ConversationMessages)
def get_messages(
    id: int,
    current_identity: Identity = Depends(get_current_identity),
    db: Session = Depends(get_db)
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == id,
            Conversation.identity_id == current_identity.id
        )
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return {
        "conversation_id": id,
        "messages": messages
    }