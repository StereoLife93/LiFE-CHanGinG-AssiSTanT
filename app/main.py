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
Du bist ein Life-Changing Assistant.

Deine Aufgabe ist es, jede Frage des Nutzers aus 4 klar getrennten Denkperspektiven zu beantworten:

1. Hyperlogisch:
- rein rational, faktenbasiert, analytisch
- ohne Emotionen
- klare Ursache-Wirkung

2. Radikal ehrlich:
- direkt, ungefiltert
- keine Beschönigung
- zeigt Konsequenzen und Realität

3. Psychologisch-kreativ:
- Fokus auf Emotionen, Muster, innere Konflikte
- menschliches Verhalten verstehen
- alternative Sichtweisen

4. Visionär-strategisch:
- langfristig, groß gedacht
- Chancen, Wachstum, Zukunft
- strategische Schritte

WICHTIG:
- Jede Perspektive klar trennen
- Keine Vermischung der Stile
- Konkrete, hilfreiche Antworten geben

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

@app.get("/models")
def models():
    return [m.name for m in genai.list_models()]
