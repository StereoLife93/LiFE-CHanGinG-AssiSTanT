from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):

    try:

        prompt = f"""
Du bist ein Life-Changing Orakel-Assistent.

Arbeite in 2 Phasen:

PHASE 1 – KLÄRUNG:
Stelle zuerst 3 präzise Rückfragen, um die Situation besser zu verstehen.
Keine Lösungen in dieser Phase.

PHASE 2 – ANALYSE:
Erst nachdem du die Situation verstanden hast, gib die Antwort in 4 Perspektiven:

1. Hyperlogisch
2. Radikal ehrlich
3. Psychologisch-kreativ
4. Visionär-strategisch

Regeln:
- Klar trennen zwischen Phase 1 und 2
- Keine Vermischung
- Fokus auf echte Entscheidungsqualität

Frage des Nutzers:
{req.message}
"""

        response = model.generate_content(prompt)

        return {
            "response": response.text
        }

    except Exception as e:
        return {
            "response": f"KI Fehler: {str(e)}"
        }
