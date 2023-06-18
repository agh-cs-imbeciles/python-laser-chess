from __future__ import annotations
import websockets
from websockets.exceptions import ConnectionClosedOK
from app.client import Sender, Receiver


class Connection:
    URI: str = "ws://127.0.0.1:8000"
    TIMEOUT_S: float = 15 * 60

    @classmethod
    async def create_game(cls) -> dict[str, any]:
        async with websockets.connect(cls.URI) as websocket:
            try:
                await Sender.send_create(websocket)
                return await Receiver.receive(websocket)
            except ConnectionClosedOK:
                pass

    @classmethod
    async def wait_for_player(cls) -> None:
        async with websockets.connect(cls.URI) as websocket:
            try:
                await Receiver.receive(websocket)
            except ConnectionClosedOK:
                pass

    @classmethod
    async def join_game(cls, game_id: str) -> dict[str, any]:
        async with websockets.connect(cls.URI) as websocket:
            try:
                await Sender.send_join(websocket, game_id)
                return await Receiver.receive(websocket)
            except ConnectionClosedOK:
                pass

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
