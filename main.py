from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import identity
from routes import conversation

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

app.include_router(identity.router)
app.include_router(conversation.router)


@app.get("/")
def home():
    return {
        "message": "AI Test Generator running"
    }