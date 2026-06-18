from fastapi import FastAPI
from models import CodeRequest
from ai_service import generate_tests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (pour React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Test Generator running"}
@app.post("/generate-tests")
def generate(request: CodeRequest):

    result = generate_tests(request.code)

    return {
        "tests": result
    }
