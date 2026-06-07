import sys
import os
sys.path.append(os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import (create_tables, save_message,
                       get_all_messages, get_emotion_counts,
                       get_emotion_trend)
from model_client import predict_emotion, check_colab_health
from prompt_builder import build_prompt
from gpt_handler import get_gpt_response

# Lifespan replaces on_event startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    create_tables()
    print("Database tables created ✅")
    yield
    # Runs on shutdown (optional cleanup)
    print("App shutting down")

app = FastAPI(title="Emotion Support API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_methods     = ["*"],
    allow_headers     = ["*"],
    allow_credentials = True
)

class MessageRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "Backend running ✅"}

@app.get("/colab-status")
def colab_status():
    is_healthy = check_colab_health()
    return {
        "colab_connected": is_healthy,
        "message"        : "Colab API running ✅" if is_healthy
                           else "Colab not connected ❌"
    }

@app.post("/analyse")
def analyse(payload: MessageRequest):
    result = predict_emotion(payload.message)

    if "error" in result:
        return {
            "error"       : result["error"],
            "emotion"     : "unknown",
            "confidence"  : 0.0,
            "all_probs"   : {},
            "gpt_response": "Unable to analyse. "
                            "Check Colab is running."
        }

    emotion      = result['emotion']
    confidence   = result['confidence']
    messages     = build_prompt(payload.message, emotion)
    gpt_response = get_gpt_response(messages)
    save_message(payload.message, emotion, gpt_response)

    return {
        "emotion"     : emotion,
        "confidence"  : confidence,
        "all_probs"   : result['all_probs'],
        "gpt_response": gpt_response
    }

@app.get("/dashboard/counts")
def emotion_counts():
    return get_emotion_counts()

@app.get("/dashboard/trend")
def emotion_trend():
    return get_emotion_trend()

@app.get("/dashboard/messages")
def recent_messages():
    messages = get_all_messages(limit=50)
    return [
        {
            "id"              : m.id,
            "text_content"    : m.text_content,
            "detected_emotion": m.detected_emotion,
            "gpt_response"    : m.gpt_response,
            "timestamp"       : m.timestamp.strftime(
                                "%Y-%m-%d %H:%M:%S")
        }
        for m in messages
    ]