import asyncio
import websockets

clients = {}
next_id = 1

async def handler(websocket):
    global next_id
    client_id = next_id
    next_id += 1

    clients[websocket] = client_id
    print(f"Client {client_id} connected")

    await websocket.send(f"Ваш ID: {client_id}")

    try:
        async for message in websocket:
            print(f"[{client_id}] {message}")
            for client in clients:
                await client.send(f"[{client_id}] {message}")

    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_id} disconnected")
    finally:
        del clients[websocket]

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started on port 8765")
        await asyncio.Future()

asyncio.run(main())