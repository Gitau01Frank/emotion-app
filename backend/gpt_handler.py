import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_response(messages: list) -> str:
    try:
        response = client.chat.completions.create(
            model       = "gpt-4o-mini",
            messages    = messages,
            max_tokens  = 300,
            temperature = 0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"