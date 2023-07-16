import json
import asyncio
import websockets

async def connect_to_websocket():
    url = "ws://shareaid.pythonanywhere.com/ws/notify-socket/?token=aeda89b911650f65a1dc088aa6978ae34e023e52dfc47d40946b6a4f8df13803"

    async with websockets.connect(url) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print("Data:", data)

            if data['type'] == 'chat':
                notification = ""
                for msg in data['messages']:
                    print(msg)
                    # Do something with the notification message

# Run the WebSocket client
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
