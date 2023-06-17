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
    async def send_init(cls) -> None:
        async with websockets.connect(cls.URI) as websocket:
            await Sender.send_init(websocket)
            await Receiver.receive(websocket)

    @classmethod
    async def send_move(cls, data: dict[any, any]) -> None:
        async with websockets.connect(cls.URI) as websocket:
            try:
                await Sender.send_move(websocket, data)
                await Receiver.receive(websocket)
            except ConnectionClosedOK:
                pass
