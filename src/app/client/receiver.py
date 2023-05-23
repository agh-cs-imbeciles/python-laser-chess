import json
from common import MessageType


class Receiver:
    @classmethod
    async def receive(cls, websocket) -> None:
        message_plain = await websocket.recv()
        message = json.loads(message_plain)
        print(message)
