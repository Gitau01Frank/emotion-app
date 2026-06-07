EMOTION_PROMPTS = {
    "joy"    : "The user is feeling joyful and happy. Respond "
               "warmly and celebrate their positive emotion.",
    "sadness": "The user is feeling sad. Respond with empathy "
               "and compassion. Acknowledge their feelings "
               "and offer comfort.",
    "anger"  : "The user is feeling angry. Respond calmly and "
               "with understanding without escalating.",
    "fear"   : "The user is feeling fearful or anxious. Respond "
               "with reassurance and calm.",
    "disgust": "The user is feeling disgusted. Respond with "
               "understanding and validate their reaction "
               "constructively.",
    "shame"  : "The user is feeling ashamed. Respond with great "
               "sensitivity and without judgement.",
    "guilt"  : "The user is feeling guilty. Respond with "
               "compassion without reinforcing self-blame."
}

def build_prompt(user_message: str, emotion: str) -> list:
    context = EMOTION_PROMPTS.get(
        emotion,
        "Respond empathetically to the user."
    )
    return [
        {
            "role"   : "system",
            "content": f"You are a compassionate emotional support "
                       f"assistant. {context} Keep responses concise, "
                       f"warm and supportive. Do not diagnose or give "
                       f"medical advice."
        },
        {
            "role"   : "user",
            "content": user_message
        }
    ]