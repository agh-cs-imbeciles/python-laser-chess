from __future__ import annotations

import asyncio

import websockets
from websockets.exceptions import ConnectionClosedOK
from app.client import Sender, Receiver


class ConnectionMeta(type):
    _instances: dict[ConnectionMeta, Connection] = {}

    def __call__(cls, *args, **kwargs) -> Connection:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Connection(metaclass=ConnectionMeta):
    URI: str = "ws://127.0.0.1:8000"
    TIMEOUT_S: float = 15 * 60

    def __init__(self) -> None:
        self.__websocket = None

    async def create_game(self) -> dict[str, any]:
        self.__websocket = await websockets.connect(Connection.URI)
        try:
            await Sender.send_create(self.__websocket)
            return await Receiver.receive(self.__websocket)
        except ConnectionClosedOK:
            pass

    async def join_game(self, game_id: str) -> dict[str, any]:
        self.__websocket = await websockets.connect(Connection.URI)
        try:
            await Sender.send_join(self.__websocket, game_id)
            return await Receiver.receive(self.__websocket)
        except ConnectionClosedOK:
            pass

    async def wait_for_player(self, game_id: str) -> None:
        try:
            response = await Receiver.receive(self.__websocket)
            print(response)
        except ConnectionClosedOK as exception:
            pass

    async def communicate_move(self, data: dict[any, any], player_id: str | None) -> dict[str, any]:
        if not player_id:
            raise ValueError("Player ID is None")

        try:
            await Sender.send_move(self.__websocket, data, player_id)
            return await Receiver.receive(self.__websocket)
        except ConnectionClosedOK:
            pass
