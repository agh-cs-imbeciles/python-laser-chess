import asyncio
import websockets
from app.client import Sender, Receiver


class Connection:
    URI: str = "ws://127.0.0.1:8000"

    def __init__(self) -> None:
        self.__websocket = None

    async def connect(self) -> None:
        self.__websocket = await websockets.connect(Connection.URI)

    @classmethod
    async def send_init(cls) -> None:
        async with websockets.connect(Connection.URI) as websocket:
            await Sender.send_init(websocket)
            await Receiver.receive(websocket)

    @classmethod
    async def send_move(cls, data: dict[any, any]) -> None:
        async with websockets.connect(Connection.URI) as websocket:
            await Sender.send_move(websocket, data)
            await Receiver.receive(websocket)
