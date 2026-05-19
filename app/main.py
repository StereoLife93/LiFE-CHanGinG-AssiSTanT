from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):

    try:
        # TEST RESPONSE OHNE KI (zum prüfen ob Backend stabil läuft)
        return {
            "response": f"Backend funktioniert. Du hast gesagt: {req.message}"
        }

    except Exception as e:
        return {
            "response": f"Fehler im Backend: {str(e)}"
        }
