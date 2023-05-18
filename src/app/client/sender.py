import json
import websockets
from app.client import Connection


class Sender:
    @staticmethod
    async def send(data: dict[any, any]):
        async with websockets.connect(Connection.URI) as websocket:
            print(data)
            print(json.dumps(data))
            await websocket.send(json.dumps(data))
