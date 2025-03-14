import requests
import asyncio
import concurrent.futures
import google.generativeai as genai
from google.api_core.exceptions import InternalServerError
import speech_recognition as sr
import subprocess
import re
import nltk
from colorama import Fore, Style, init
import serial
import time

# Initialize colorama
init(autoreset=True)

# Bluetooth Configuration
SERIAL_PORT = '/dev/rfcomm0'
BAUD_RATE = 115200

# Gemini AI Setup
genai.configure(api_key="AIzaSyD02mt7Sejc3Ky6G7te8adqlk5BQr1ekj8")
model_chat = genai.GenerativeModel("gemini-2.0-flash")

class BLEConnection:
    """Handles Bluetooth communication with ESP32."""
    
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None

    def connect(self):
        """Establish Bluetooth connection."""
        if not self.serial_connection or not self.serial_connection.is_open:
            try:
                self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
                print(f"Connected to {self.port}")
            except serial.SerialException as e:
                print(f"Connection Error: {e}")

    def send_message(self, message):
        """Send a message via Bluetooth."""
        self.connect()
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(message.encode())
                print(f"Sent: {message.strip()}")
                time.sleep(1)  # Wait for response
                if self.serial_connection.in_waiting > 0:
                    response = self.serial_connection.read(self.serial_connection.in_waiting).decode()
                    print(f"Received: {response}")
            except serial.SerialException as e:
                print(f"Error sending message: {e}")

    def disconnect(self):
        """Close Bluetooth connection."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Disconnected.")

# Initialize Bluetooth Connection
ble_connection = BLEConnection(SERIAL_PORT, BAUD_RATE)

# User and Bot Configuration
bot_name = input("Enter bot name: ")
user_name = "Avin"

chat_prompt = f"""
You are {bot_name}, a friendly and interactive AI companion.
You respond in a warm and playful manner, providing assistance and entertainment.
You also handle smart commands like playing music, scheduling tasks, and controlling smart devices.
Your responses should be short, engaging, and natural.

User: {user_name}
"""

chat = model_chat.start_chat(history=[{"role": "user", "parts": chat_prompt}, {"role": "model", "parts": "Sure! I'm ready to chat."}])

def strip_markdown(md_text):
    """Removes markdown syntax from text."""
    md_text = re.sub(r'[#*_`!\[\]\(\)]', '', md_text)  # Remove markdown characters
    return ' '.join(md_text.split())  # Normalize whitespace

def speak_with_piper(text):
    """Converts text to speech using Piper TTS."""
    clean_text = strip_markdown(text).replace("\n", " ")
    if clean_text.strip():
        try:
            process = subprocess.Popen(["./piper", "--model", "en_US-hfc_female-medium.onnx", "--output_file", "-"],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = process.communicate(input=clean_text.encode())
            subprocess.Popen(["aplay"], stdin=subprocess.PIPE).communicate(input=stdout)
        except Exception as e:
            print(f"{Fore.YELLOW}TTS Error: {e}")

def process_chat(user_input):
    """Handles chatbot interaction."""
    if not user_input.strip():
        return "Error: Empty input."
    try:
        response = chat.send_message(user_input)
        response_text = response.text.lower()
        
        if "yes" in response_text[:3]:
            ble_connection.send_message("yes")
        elif "no" in response_text[:2]:
            ble_connection.send_message("no")

        return response.text
    except InternalServerError as e:
        return f"ChatBot Error: {e}"

def listen_for_input():
    """Listens for user speech input and returns recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"{Fore.GREEN}Listening...")
        try:
            audio = recognizer.listen(source)
            print(f"{Fore.RED}Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print(f"{Fore.YELLOW}Could not understand. Try again.")
            return None
        except sr.RequestError as e:
            print(f"{Fore.YELLOW}Speech API error: {e}")
            return None

async def handle_input():
    """Handles asynchronous speech input processing."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            user_input = listen_for_input()
            if user_input:
                response = await asyncio.get_event_loop().run_in_executor(executor, process_chat, user_input)
                print(f"{Fore.CYAN}Bot: {response}")
                speak_with_piper(response)

if __name__ == "__main__":
    asyncio.run(handle_input())
