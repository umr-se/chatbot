from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI(
    title="chatbot",
    version="1.0"
)

def get_fact():
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    return response.json()["text"]

def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = response.json()
    return f"{data['setup']} ... {data['punchline']}"

def get_dog_image():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    return response.json()['message']
    

def chatbot_response(user_input: str) -> str:
    user_input = user_input.lower().strip()

    greetings = ["hello", "hi", "hey", "hy"]
    casual_checkins = [
        "what's up", "whats up", "what is up",
        "what's happening", "whats happening",
        "how are you", "how's it going", "hows it going",
        "how are things", "how's things", "hows things"
    ]

    if any(phrase in user_input for phrase in greetings):
        if "help" in user_input:
            return "Hi there! How can I help you today?"
        elif "joke" in user_input:
            return "Hi there! Here's a joke:\n" + get_joke()
        else:
            return "Hi there! How can I help you today?"

    if any(phrase in user_input for phrase in casual_checkins):
        return "I'm doing great, thanks for asking! How about you?"

    if "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"

    if "joke" in user_input:
        return get_joke()
    
    if "fact" in user_input:
        return get_fact()
    if "dog" in user_input and "image" in user_input:
        return get_dog_image()

    if "help" in user_input:
        return "Sure, I'm here to help! What do you need?"

    if "your name" in user_input or "who are you" in user_input:
        return "I'm a simple chatbot built with FastAPI."

    if "weather" in user_input:
        return "Sorry, I can't provide real-time weather yet!"

    # Fallback
    return "Sorry, I didn't understand that. Can you rephrase?"

@app.get('/')
async def home():
    return{"welcome!!"}

@app.post("/chat")
async def chat_endpoint(message: str = Form(...)):
    bot_reply = chatbot_response(message)
    return {"response": bot_reply}
