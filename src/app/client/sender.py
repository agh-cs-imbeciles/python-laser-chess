from __future__ import annotations
import json
from common import MessageType


class Sender:
    @classmethod
    async def send_create(cls, websocket) -> None:
        message = {
            "messageType": str(MessageType.CREATE)
        }
        await cls.__send(websocket, message)

    @classmethod
    async def send_join(cls, websocket, game_id: str) -> None:
        message = {
            "messageType": str(MessageType.JOIN),
            "gameId": game_id
        }
        print(message)
        await cls.__send(websocket, message)

    # @classmethod
    # async def send_init(cls, websocket) -> None:
    #     message = {
    #         "messageType": str(MessageType.INIT)
    #     }
    #     await cls.__send(websocket, message)

    @classmethod
    async def send_move(cls, websocket, data: dict[any, any], player_id: str | None) -> None:
        message = {
            "messageType": str(MessageType.MOVE),
            "playerId": player_id,
            "data": data
        }
        await cls.__send(websocket, message)

    @classmethod
    async def __send(cls, websocket, message: dict[str, any]) -> None:
        # print(json.dumps(message))
        await websocket.send(json.dumps(message))
