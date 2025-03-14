import json
from prompts import load_user_data, generate_prompt
from chatbot import initialize_chat_with_history,generate_chat_responses ,chat, chatbot_model ,load_chat_history,save_chat_history , HISTORY_FILE_PATH

def main():
    file_path = "usersinfo.json"
    try:
        data = load_user_data(file_path)
        prompt = generate_prompt(data)

        # Load chat history
        history = load_chat_history()
        
        # Check if initial prompt exists
        if any(entry["role"] == "user" and entry["parts"] == prompt for entry in history):
            print("Initial history is already set. Continuing with the chat...")
        else:
            print("Setting initial history...")
            initialize_chat_with_history(chatbot_model , prompt, "sure")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print("Error: The JSON file is not properly formatted.")
    except KeyError as e:
        print(f"Error: Missing expected key in JSON data: {e}")
    




    while(1):
        user_input = input("enter the prompt")
        history.append({"role": "user", "parts": user_input})

        # Generate response
        ai_response = generate_chat_responses(chat(model_instance=chatbot_model), user_input).text
        print(ai_response)

        # Append AI response to history
        history.append({"role": "assistant", "parts": ai_response})

        # Save updated history
        save_chat_history(history)
if __name__ == "__main__":
    main()
