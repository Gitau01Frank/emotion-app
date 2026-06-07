import requests
import os
from dotenv import load_dotenv

load_dotenv()

COLAB_API_URL = os.getenv("COLAB_API_URL")

def predict_emotion(text: str) -> dict:
    try:
        response = requests.post(
            f"{COLAB_API_URL}/predict",
            json    = {"message": text},
            timeout = 30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "emotion"   : "unknown",
                "confidence": 0.0,
                "all_probs" : {},
                "error"     : f"Colab API error {response.status_code}"
            }

    except requests.exceptions.ConnectionError:
        return {
            "emotion"   : "unknown",
            "confidence": 0.0,
            "all_probs" : {},
            "error"     : "Cannot connect to Colab. "
                          "Make sure notebook is running."
        }
    except requests.exceptions.Timeout:
        return {
            "emotion"   : "unknown",
            "confidence": 0.0,
            "all_probs" : {},
            "error"     : "Colab API timed out. Try again."
        }

def check_colab_health() -> bool:
    try:
        response = requests.get(
            f"{COLAB_API_URL}/health",
            timeout = 10
        )
        return response.status_code == 200
    except:
        return False