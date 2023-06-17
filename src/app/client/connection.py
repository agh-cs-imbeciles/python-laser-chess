from __future__ import annotations
import asyncio
import websockets
from websockets.client import WebSocketClientProtocol
from app.client import Sender, Receiver


class Connection:
    URI: str = "ws://127.0.0.1:8000"
    TIMEOUT_S: float = 15 * 60

    def __init__(self) -> None:
        self.__websocket: WebSocketClientProtocol | None = None

    def is_established(self) -> bool:
        return isinstance(self.__websocket, WebSocketClientProtocol)

    async def connect(self) -> None:
        try:
            self.__websocket = await websockets.connect(Connection.URI, open_timeout=Connection.TIMEOUT_S, close_timeout=Connection.TIMEOUT_S)
        except asyncio.TimeoutError:
            print("huh")

    async def ping(self) -> None:
        await self.__websocket.ping()

    async def send_init(self) -> None:
        await Sender.send_init(self.__websocket)
        await Receiver.receive(self.__websocket)
        pass

    async def send_move(self, data: dict[any, any]) -> None:
        await Sender.send_move(self.__websocket, data)
        await Receiver.receive(self.__websocket)
