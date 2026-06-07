import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def check_colab_status():
    try:
        return requests.get(
            f"{BASE_URL}/colab-status",
            timeout = 10
        )
    except:
        return None

def send_message(message: str):
    return requests.post(
        f"{BASE_URL}/analyse",
        json    = {"message": message},
        timeout = 30
    )

def get_emotion_counts():
    return requests.get(
        f"{BASE_URL}/dashboard/counts",
        timeout = 10
    )

def get_emotion_trend():
    return requests.get(
        f"{BASE_URL}/dashboard/trend",
        timeout = 10
    )

def get_recent_messages():
    return requests.get(
        f"{BASE_URL}/dashboard/messages",
        timeout = 10
    )