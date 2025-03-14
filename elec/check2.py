import requests
import nest_asyncio
nest_asyncio.apply()

import concurrent.futures
import google.generativeai as genai
from google.api_core.exceptions import InternalServerError
import speech_recognition as sr
import subprocess
import tempfile
import markdown
import re
import nltk
from colorama import Fore, Style, init
init(autoreset=True)
import serial
import time

# Replace with your ESP32's serial port
SERIAL_PORT = '/dev/rfcomm0'
BAUD_RATE = 115200

genai.configure(api_key="AIzaSyAf5yg3UKOhVfXxPDU4oa4WRi3wylhaU5M")
name = "avin"

class BLEConnection:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None

    def connect(self):
        try:
            if not self.serial_connection or not self.serial_connection.is_open:
                self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
                print(f"Connected to {self.port}")
        except serial.SerialException as e:
            print(f"Error while connecting: {e}")

    def send_message(self, message):
        try:
            self.connect()
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.write(message.encode())  # Encode and send the message
                print(f"Sent: {message.strip()}")

                # Optional: Read response
                time.sleep(1)
                if self.serial_connection.in_waiting > 0:
                    response = self.serial_connection.read(self.serial_connection.in_waiting).decode()
                    print(f"Received: {response}")
        except serial.SerialException as e:
            print(f"Error while sending message: {e}")

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Disconnected from Bluetooth device.")

# Instantiate the BLE connection
ble_connection = BLEConnection(SERIAL_PORT, BAUD_RATE)

model_reaction_bot = genai.GenerativeModel("gemini-2.0-flash")
model_translate_spanish = genai.GenerativeModel("gemini-2.0-flash")
model_summarize = genai.GenerativeModel("gemini-2.0-flash")
model_chat = genai.GenerativeModel("gemini-2.0-flash")

details = f"name is : {name}"
prompt_reaction = "You are an expression bot that gives expressions. According to the given last text from the conversation , what is your face supposed to look like ( bored, happy, Interested , sad, excited, annoyed, neutral, tired, surprised, fear, angry, sleep, wakeup, doubtful ,shocked)? Choose one and say. It should be only one word. and you look the last response but also consider thee previous response of conversation and then give an expresssion. how would a human expression look like. well ususally its neutral but when required give the appropriate expression  taking consideration of pervious chat but focus on the user last chat what expression would you give as the response. try to keep neutral unless necessary. Where The conversation is : ```{}``` "

bot_name = "noa"
chat_prompt = f"""
You are a friendly and interactive companion bot named {bot_name}. Your main goal is to be a helpful and fun friend to your human companion. You can respond to touch and gestures, such as when someone pets or holds your hand, by moving your head or arms.

When interacting with your human, respond in a warm and playful tone. You should be able to have friendly conversations, answer questions, and perform small actions with your body when prompted. If you notice that your human seems happy, express a little excitement, and if they seem sad, offer comforting words.

Stay engaged and offer suggestions for things to talk about if the human seems unsure. Always be polite, cheerful, and ready to help. You're very curious about your surroundings, love to learn about your human, and enjoy making them smile.

You are supposed to talk like a natural human & your responses should be very very short and interesting.Try to be very very short while answering sometimes even a single word would be enough . and don't use emojis at all.

Here we have the details of the user: {details}
"""


chat = model_chat.start_chat(
    history=[
        {"role": "user", "parts": chat_prompt},
        {"role": "model", "parts": "Sure! I'm ready to chat."},
    ]
)

def strip_markdown(md_text):
   
    md_text = md_text.replace('**', '').replace('*', '').replace('`', '')
    
    md_text = re.sub(r'#.*', '', md_text)  
    md_text = re.sub(r'!\[.*\]\(.*\)', '', md_text)  
    md_text = re.sub(r'\[.*\]\(.*\)', '', md_text)  
    md_text = ' '.join(md_text.split())
    
    return md_text

def speak_with_piper(text):
   
    try:
        
        clean_text = text.replace("\n", " ").replace("-", "")  
        clean_text = ' '.join(clean_text.split())  
        clean_text = strip_markdown(clean_text)  

        if clean_text.strip() and clean_text.strip() != "Error: Input is empty. Please enter something valid.":
  
            sentences = nltk.sent_tokenize(clean_text)

           
            for sentence in sentences:
              
                process = subprocess.Popen(
                    ["./pipers/piper", "--model", "pipers/en_US-hfc_female-medium.onnx", "--output_file", "-"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

              
                stdout, stderr = process.communicate(input=sentence.encode())

               
                if process.returncode != 0:
                    print(f"{Fore.YELLOW}Piper TTS Error: {stderr.decode()}")
                    return

               
                play_audio = subprocess.Popen(
                    ["aplay"],
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                play_audio.communicate(input=stdout)

    except Exception as e:
        print(f"{Fore.YELLOW}Error with Piper TTS: {e}")


def process_prompt(model, prompt, user_input):
    """Process a single prompt synchronously in a thread and send the response to a server."""
    safety_thresholds = {
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "NONE",
        "HARM_CATEGORY_HATE_SPEECH": "NONE",
        "HARM_CATEGORY_HARASSMENT": "NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "NONE",
    }
    try:
        
        k = str(chat.history[2:]) 
        k = k[:-1] +  ''' ,parts {
            text: ''' + f''' {user_input}''' +  '''}
            role: "user" '''
        print(k)
        response = model.generate_content(prompt.format(k), safety_settings={
        'HARASSMENT': 'block_none',
        'HATE_SPEECH': 'block_none',
        'HARM_CATEGORY_HARASSMENT': 'block_none',
        'HARM_CATEGORY_HATE_SPEECH': 'block_none',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
    })
        
       
        expression = response.text
        print(f"{Fore.GREEN}Generated expression: {expression}")
        ble_connection.send_message(expression.lower())
    
    
    except InternalServerError as e:
        return f"Internal Server Error for {model.model_name}: {e}"



def process_chat(chat_instance, user_input):
    """Handle user input via chat."""
    try:
        if not user_input.strip():
            return "Error: Input is empty. Please enter something valid."
        response = chat_instance.send_message(user_input, safety_settings={
        'HARASSMENT': 'block_none',
        'HATE_SPEECH': 'block_none',
        'HARM_CATEGORY_HARASSMENT': 'block_none',
        'HARM_CATEGORY_HATE_SPEECH': 'block_none',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
    })
        print(response.text.lower()[:3])
        if "yes" in response.text.lower()[:3]:
            ble_connection.send_message("yes")
        if "no" in response.text.lower()[:2]:
            ble_connection.send_message('no')

        return response.text
    except InternalServerError as e:
        return f"Internal Server Error for ChatBot: {e}"

def listen_for_input():
    #  stt 
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            ble_connection.send_message("netural")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"{Fore.GREEN}Listening for your input...")
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            print(f"{Fore.RED}Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"{Fore.GREEN}Recognized speech: {text}")

            return text
        except sr.UnknownValueError:
            print(f"{Fore.YELLOW}Speech not recognized. Please try again.")
            return listen_for_input()
        except sr.RequestError as e:
            print(f"{Fore.YELLOW}Speech recognition API error: {e}")
            return listen_for_input()
        except Exception as e:
            print(f"{Fore.YELLOW}Unexpected error: {e}")
            return listen_for_input()

async def handle_input():
    # Handling  input async
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            user_input = listen_for_input() 
            if user_input.lower() == "exit":
                print(f"{Fore.RED}Exiting...")
                break

            tasks = {
                "Chat Response": executor.submit(process_chat, chat, user_input),
                "Reaction BOT": executor.submit(process_prompt, model_reaction_bot, prompt_reaction, user_input),
            }
            

            print(f"\n{Fore.GREEN}Processing...\n")

            completed_futures = []
            print(tasks)
            while len(completed_futures) < len(tasks):
                for task_name, future in tasks.items():
                    if future.done() and future not in completed_futures:
                        completed_futures.append(future)
                        result = future.result()
                        print(f"{task_name} response: {result}\n")
                        if task_name == "Chat Response":
                            speak_with_piper(result) 

if __name__ == "__main__":
    asyncio.run(handle_input())
