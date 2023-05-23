import json
import websockets
from app.client import Connection
from common import MessageType


class Sender:
    @staticmethod
    async def send_init() -> None:
        pass

    @staticmethod
    async def send_move(data: dict[any, any]) -> None:
        async with websockets.connect(Connection.URI) as websocket:
            message = {
                "messageType": str(MessageType.MOVE),
                "data": data
            }
            print(json.dumps(message))
            await websocket.send(json.dumps(message))
