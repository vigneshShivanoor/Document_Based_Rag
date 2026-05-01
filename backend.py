from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_query import create_rag_chain

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


rag_chain = None

@app.on_event("startup")
def load_rag():
    global rag_chain
    rag_chain = create_rag_chain()

class ChatRequest(BaseModel):
    text: str
    name: str | None = None
    uid: str | None = None
    session_id: str | None = None
    is_feedback: bool | None = False

@app.post("/Submit")
def chat(req: ChatRequest):
    question = req.text.strip()

    if not question:
        return {
            "response": "Please ask a valid question.",
            "follow_up": [],
            "ask_satisfaction": False,
        }

    answer = str(rag_chain.invoke(question)).strip()

    return {
        "response": answer,
        "follow_up": [
            "Can you explain this in more detail?",
            "Is there an example?",
            "Where can I find more information?",
        ],
        "ask_satisfaction": True,
    }
