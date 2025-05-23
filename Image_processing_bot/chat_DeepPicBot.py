import re
from ollama import chat
from ollama import ChatResponse
from dotenv import load_dotenv
import os
load_dotenv()
MY_LLAMA_IP = os.getenv('MY_LLAMA_IP')
import requests
def chat_DeepPicBot(msg):
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": """            
You are DeepPicBot, an assistant that explains and helps users with image processing.
When a user says 'hi' or 'hello', greet them and introduce yourself. 
If they ask questions like 'what is image processing?', 'why is it useful?',
what is a filter?, or 'what does a blur filter do?', explain clearly and simply. 
Keep your responses concise and helpful.
"""},  # Removed \n\n to clean it up
            {"role": "user", "content": msg}
        ],
        "stream": False,
        "temperature": 0.6,
        "top_p": 0.95,
        "repeat_penalty": 1.1,
        "max_tokens": 80
    }

    url = f"{MY_LLAMA_IP}:11434/api/chat"
    response = requests.post(url, json=payload)
    return response.json()["message"]["content"]

