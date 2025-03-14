import google.generativeai as genai
import json
from time import sleep

# Configure the API key
genai.configure(api_key="AIzaSyAf5yg3UKOhVfXxPDU4oa4WRi3wylhaU5M")

# Initialize different model instances
chatbot_model = genai.GenerativeModel("gemini-2.0-flash")
# reaction_bot_model = genai.GenerativeModel("gemini-2.0-flash")
# translation_model = genai.GenerativeModel("gemini-2.0-flash")
# summarization_model = genai.GenerativeModel("gemini-2.0-flash")


# File to store chat history
HISTORY_FILE_PATH = "history.json"

def load_chat_history():
    """Load chat history from history.json file."""
    try:
        with open(HISTORY_FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_chat_history(chat_history):
    """Save chat history to history.json file."""
    with open(HISTORY_FILE_PATH, "w") as file:
        json.dump(chat_history, file, indent=4)

def append_message_to_history(role, message):
    """Append a new message to chat history and save it."""
    chat_history = load_chat_history()
    chat_history.append({"role": role, "parts": message})
    save_chat_history(chat_history)

# Safety settings for content filtering
safety_settings = {
    'HARASSMENT': 'block_none',
    'HATE_SPEECH': 'block_none',
    'HARM_CATEGORY_HARASSMENT': 'block_none',
    'HARM_CATEGORY_HATE_SPEECH': 'block_none',
    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
    'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
}

def generate_ai_response(user_prompt):
    """Generate a response using the chatbot model."""
    return chatbot_model.generate_content(user_prompt, safety_settings=safety_settings)

def generate_chat_responses(chat , prompt):
    global safety_settings
    return chat.send_message(prompt,  safety_settings=safety_settings)




def chat(model_instance):
    chat_history = load_chat_history()
    return model_instance.start_chat(
        history=chat_history)


def initialize_chat_with_history(model_instance, initial_user_message, initial_model_response):
    """
    Check if the initial chat history is already stored.
    If not, store it and return a new chat session.
    """
    chat_history = load_chat_history()
    print(chat_history)

    # Check if the initial user message is already in history
    for entry in chat_history:
        if entry["role"] == "user" and entry["parts"] == initial_user_message:
            return model_instance
    
    # Otherwise, add the initial messages to history
    append_message_to_history("user", initial_user_message)
    append_message_to_history("model", initial_model_response)

    return model_instance.start_chat(
        history=chat_history
    )
