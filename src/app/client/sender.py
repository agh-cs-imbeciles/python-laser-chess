from __future__ import annotations
import json
from common import MessageType


class Sender:
    @classmethod
    async def send_init(cls, websocket) -> None:
        message = {
            "messageType": str(MessageType.INIT)
        }
        # print(json.dumps(message))
        await websocket.send(json.dumps(message))

    @classmethod
    async def send_move(cls, websocket, data: dict[any, any], player_id: str | None) -> None:
        message = {
            "messageType": str(MessageType.MOVE),
            "playerId": player_id,
            "data": data
        }
        # print(json.dumps(message))
        await websocket.send(json.dumps(message))
