from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/chat")
def chat(req: ChatRequest):

    try:
        response = model.generate_content(req.message)

        return {
            "response": response.text
        }

    except Exception as e:
        return {
            "response": f"KI Fehler: {str(e)}"
        }
