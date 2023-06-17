import json
from common import MessageType


class Receiver:
    @classmethod
    async def receive(cls, websocket) -> dict[str, any]:
        message_plain = await websocket.recv()
        message = json.loads(message_plain)
        return message
