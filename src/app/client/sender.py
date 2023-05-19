import json
import websockets
from app.client import Connection


class Sender:
    @staticmethod
    async def send_init() -> None:
        pass

    @staticmethod
    async def send_move(data: dict[any, any]) -> None:
        async with websockets.connect(Connection.URI) as websocket:
            print(json.dumps(data))
            await websocket.send(json.dumps(data))
