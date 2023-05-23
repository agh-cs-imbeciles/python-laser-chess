import json
from common import MessageType


class Sender:
    @classmethod
    async def send_init(cls, websocket) -> None:
        message = {
            "messageType": str(MessageType.INIT)
        }
        print(json.dumps(message))
        await websocket.send(json.dumps(message))

    @classmethod
    async def send_move(cls, websocket, data: dict[any, any]) -> None:
        message = {
            "messageType": str(MessageType.MOVE),
            "data": data
        }
        print(json.dumps(message))
        await websocket.send(json.dumps(message))
