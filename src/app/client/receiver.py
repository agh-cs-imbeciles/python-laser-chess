import json
from asyncio import wait_for


class Receiver:
    @classmethod
    async def receive(cls, websocket) -> dict[str, any]:
        message_plain = await websocket.recv()
        message = json.loads(message_plain)
        return message

    @classmethod
    async def receive_wait(cls, websocket) -> dict[str, any]:
        message_plain = await wait_for(websocket.recv(), None)
        message = json.loads(message_plain)
        return message
