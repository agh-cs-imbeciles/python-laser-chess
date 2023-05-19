import json
import websockets
from app.client import Connection
from common import Status


class Sender:
    @staticmethod
    async def send_init() -> None:
        pass

    @staticmethod
    async def send_move(data: dict[any, any]) -> None:
        async with websockets.connect(Connection.URI) as websocket:
            data["status"] = str(Status.MOVE)
            print(json.dumps(data))
            await websocket.send(json.dumps(data))
