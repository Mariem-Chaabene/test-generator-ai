from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.conversation import Conversation
from schemas.conversation import ConversationCreate

from models.requests import CodeRequest
from services.ai_service import generate_tests

router = APIRouter(
    prefix="/conversation",
    tags=["conversation"]
)

@router.post("")
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db)
):

    conversation = Conversation(
        identity_id=request.identity_id
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id
    }

@router.post("/generate-tests")
def generate(request: CodeRequest):

    tests = generate_tests(request.code)

    return {
        "tests": tests
    }

@router.post("/upload-java")
async def upload_java(file: UploadFile = File(...)):

    content = await file.read()

    java_code = content.decode("utf-8")

    tests = generate_tests(java_code)

    return {
        "filename": file.filename,
        "tests": tests
    }