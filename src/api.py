from fastapi import FastAPI
from pydantic import BaseModel

from src.predict_intent import predict_intent
from src.rag import retrieve_response


app = FastAPI(
    title="Sonelgaz Customer Service Chatbot API",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Sonelgaz Customer Service Chatbot",
    }


@app.post("/chat")
def chat(request: ChatRequest):

    predictions = predict_intent(request.message)

    intent = predictions[0][0]
    confidence = float(predictions[0][1])

    rag_result = retrieve_response(intent)

    return {
        "message": request.message,
        "intent": intent,
        "confidence": confidence,
        "response": rag_result["response"],
        "found": rag_result["found"],
        "source": rag_result["source"],
        "source_url": rag_result["source_url"],
    }