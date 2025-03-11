import serial
import time

# Replace with your ESP32's serial port
SERIAL_PORT = '/dev/rfcomm0'
BAUD_RATE = 115200

def main():
    try:
        # Open the serial port
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT}")
            for i in range(0,10):
                # Send a message
                message = "Hello, ESP32!\n"
                ser.write(message.encode())  # Encode the message as bytes
                print(f"Sent: {message.strip()}")

                # Optionally, wait for a response
                time.sleep(0.2)
            
    
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
