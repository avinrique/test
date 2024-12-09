# import asyncio
# import websockets

# async def websocket_client():
#     uri = "ws://10.250.33.131/ws" 
#     async with websockets.connect(uri) as websocket:
#         await websocket.send("Hello from laptop!")
#         response = await websocket.recv()
#         print(f"Received from ESP8266: {response}")

# # Run the client
# asyncio.run(websocket_client())











# import asyncio
# import websockets

# async def websocket_client():
#     uri = "ws://10.250.33.131/ws"  # Replace with your ESP8266's IP address
#     try:
#         async with websockets.connect(uri) as websocket:
#             # Send a message to the ESP8266 WebSocket server
#             await websocket.send("Hello from laptop!")
#             print("Message sent to the ESP8266!")

#             # Wait for a response from the server
#             response = await websocket.recv()
#             print(f"Received from ESP8266: {response}")

#     except websockets.exceptions.ConnectionClosedError as e:
#         print(f"Connection closed unexpectedly: {e}")
#     except asyncio.TimeoutError:
#         print("Connection timed out. Please check the server's availability.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Run the WebSocket client
# if __name__ == "__main__":
#     asyncio.run(websocket_client())






















# import asyncio
# import websockets

# async def websocket_client():
#     uri = "ws://10.250.33.131/ws"  # Replace with your ESP8266's IP address
#     try:
#         async with websockets.connect(uri) as websocket:
#             print("Connected to the WebSocket server!")

#             while True:
#                 # Send a message to the server
#                 message = input("Enter a message to send (type 'exit' to close): ")
#                 if message.lower() == 'exit':
#                     print("Closing connection...")
#                     break

#                 await websocket.send(message)
#                 print(f"Sent: {message}")

#                 # Wait for a response from the server
#                 response = await websocket.recv()
#                 print(f"Received: {response}")

#     except websockets.exceptions.ConnectionClosedError as e:
#         print(f"Connection closed unexpectedly: {e}")
#     except asyncio.TimeoutError:
#         print("Connection timed out. Please check the server's availability.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Run the WebSocket client
# if __name__ == "__main__":
#     asyncio.run(websocket_client())




import asyncio
import websockets

async def websocket_client(uri, message_queue):
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the WebSocket server!")

            async def send_messages():
                while True:
                    # Get a message from the queue
                    message = await message_queue.get()
                    if message == "exit":
                        print("Closing connection...")
                        break

                    await websocket.send(message)
                    print(f"Sent: {message}")

            async def receive_messages():
                while True:
                    response = await websocket.recv()
                    print(f"Received: {response}")

            # Run send and receive tasks concurrently
            await asyncio.gather(send_messages(), receive_messages())

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")
    except asyncio.TimeoutError:
        print("Connection timed out. Please check the server's availability.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def another_task(message_queue):
    counter = 1
    while True:
        # Generate a message
        counter += 1
        a=input("ennter ") 

        # Put the message into the queue
        await message_queue.put(a)
        print(f"Generated and queued: {a}")

        await asyncio.sleep(2)  # Simulate message generation delay

async def main():
    uri = "ws://10.250.33.131/ws"  # Replace with your ESP8266's IP address
    message_queue = asyncio.Queue()  # Queue to share messages between tasks

    await asyncio.gather(
        websocket_client(uri, message_queue),
        another_task(message_queue)
    )

if __name__ == "__main__":
    asyncio.run(main())
