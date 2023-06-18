from __future__ import annotations
import websockets
from websockets.exceptions import ConnectionClosedOK
from app.client import Sender, Receiver


class Connection:
    URI: str = "ws://127.0.0.1:8000"
    TIMEOUT_S: float = 15 * 60

    # def __init__(self) -> None:
    #     self.__websocket: WebSocketClientProtocol | None = None
    #
    # def is_established(self) -> bool:
    #     return isinstance(self.__websocket, WebSocketClientProtocol)

    # async def connect(self) -> None:
    #     try:
    #         self.__websocket = await websockets.connect(Connection.URI)
    #     except asyncio.TimeoutError:
    #         print("huh")
    #
    # async def ping(self) -> None:
    #     await self.__websocket.ping()

    @classmethod
    async def communicate_init(cls) -> dict[str, any]:
        async with websockets.connect(cls.URI) as websocket:
            await Sender.send_init(websocket)
            return await Receiver.receive(websocket)

    @classmethod
    async def communicate_move(cls, data: dict[any, any], player_id: str | None) -> dict[str, any]:
        if not player_id:
            raise ValueError("Player ID is None")

        async with websockets.connect(cls.URI) as websocket:
            try:
                await Sender.send_move(websocket, data, player_id)
                return await Receiver.receive(websocket)
            except ConnectionClosedOK:
                pass
