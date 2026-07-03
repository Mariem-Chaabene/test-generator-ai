from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from routes import identity
from request_models import CodeRequest
from services.ai_service import generate_tests
from models import Identity
from models import Conversation
from models import Message
from database import SessionLocal

// Création de l’application FastAPI
app = FastAPI(
    title="AI Test Generator",
    version="1.0.0"
)

//Ajout des routes externes: Ça importe des routes depuis un autre fichiers
app.include_router(identity.router)
app.include_router(conversation.router)
app.include_router(message.router)

//Configuration CORS: permet à ton API d’être appelée depuis :frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

//API de test
@app.get("/")
def home():
    return {"message": "AI Test Generator running"}

//API generate-tests
@app.post("/generate-tests")
def generate(request: CodeRequest):
    db = SessionLocal()
    identity = get_or_create_identity(db, request.identity_id)
    tests = generate_tests(request.code)
    return {
        "tests": tests
    }

// API upload java
@app.post("/upload-java")
async def upload_java(file: UploadFile = File(...)):
    //lire le fichier
    content = await file.read()
    //convertir en texte
    java_code = content.decode("utf-8")
    tests = generate_tests(java_code)
    return {
        "filename": file.filename,
        "tests": tests
    }


//Gestion des utilisateurs (Identity)
    def get_or_create_identity(db, identity_id: str):
    identity = db.query(Identity).filter(Identity.id == identity_id).first()
    if not identity:
        identity = Identity(id=identity_id, type="guest")
        db.add(identity)
        db.commit()
        db.refresh(identity)
    return identity

    //Gestion de conversation (chat IA)
    conversation = Conversation(
        identity_id=identity.id,
        title="New Chat"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    msg_user = Message(
    conversation_id=conversation.id,
    role="user",
    content=request.code
)

db.add(msg_user)


msg_bot = Message(
    conversation_id=conversation.id,
    role="assistant",
    content=tests
)

db.add(msg_bot)
db.commit()