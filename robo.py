import time
import random
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init()

# Sample messages to simulate AI and robotics programming
messages = [
    "[INFO] AI Module: Optimizing neural network weights...",
    "[INFO] Robot Arm: Moving to position (12, 45, 78)...",
    "[ERROR] Sensor Module: Proximity sensor disconnected!",
    "[DEBUG] Pathfinding: Calculated optimal route in 0.23s",
    "[WARNING] Battery Low: 15% remaining...",
    "[INFO] Vision System: Object recognized - ID#1245",
    "[DEBUG] Motor Control: Adjusting torque to 3.5 Nm",
    "[INFO] AI Module: Reinforcement learning cycle complete.",
    "[ERROR] Network: Connection to server lost! Reconnecting...",
    "[WARNING] Temperature High: 75°C detected in motor unit."
]

# Define initialization messages
init_messages = [
    "[INIT] Initializing environment variables...",
    "[INIT] Loading AI models and weights...",
    "[INIT] Establishing sensor connections...",
    "[INIT] Calibrating robotic arm...",
    "[INIT] Starting main control loop..."
]

# Define colors for different message types
def get_color(message):
    if "[INFO]" in message:
        return Fore.GREEN
    elif "[ERROR]" in message:
        return Fore.RED
    elif "[WARNING]" in message:
        return Fore.YELLOW
    elif "[DEBUG]" in message:
        return Fore.CYAN
    elif "[INIT]" in message:
        return Fore.MAGENTA
    else:
        return Fore.WHITE

def main():
    print(Fore.WHITE + Style.BRIGHT + "Starting Robotics Simulation...\n" + Style.RESET_ALL)

    # Display initialization messages
    for init_message in init_messages:
        print(Fore.MAGENTA + init_message + Style.RESET_ALL)
        time.sleep(1)

    print(Fore.WHITE + Style.BRIGHT + "\nInitialization Complete. Entering Main Simulation...\n" + Style.RESET_ALL)

    try:
        while True:
            message = random.choice(messages)
            color = get_color(message)
            print(color + message + Style.RESET_ALL)
            time.sleep(random.uniform(0.5, 1.5))  # Random delay between messages
    except KeyboardInterrupt:
        print(Fore.WHITE + "\nSimulation Ended." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
