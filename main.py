from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from schemas.code_request import CodeRequest
from ai_service import generate_tests

from routes import identity
from models import CodeRequest

app = FastAPI(
    title="AI Test Generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- Anciennes routes -----------

@app.get("/")
def home():
    return {
        "message": "AI Test Generator running"
    }


@app.post("/generate-tests")
def generate(request: CodeRequest):

    tests = generate_tests(request.code)

    return {
        "tests": tests
    }


@app.post("/upload-java")
async def upload_java(file: UploadFile = File(...)):

    content = await file.read()

    java_code = content.decode("utf-8")

    tests = generate_tests(java_code)

    return {
        "filename": file.filename,
        "tests": tests
    }

# ----------- Nouveau router -----------

app.include_router(identity.router)