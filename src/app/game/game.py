from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio
from app.client import Sender
from app.config import GameSettings
from app.client import Connection

if TYPE_CHECKING:
    from game import Game
    from game.piece.move import PieceMove


class GameApplication:
    def __init__(self, game: Game, **kwargs) -> None:
        self.__game = game
        self.__online = kwargs.get("online", False)

        if self.__online:
            self.__connection: Connection = Connection()
            asyncio.run(self.run_async())

    async def run_async(self) -> None:
        await self.connect()
        while True:
            print("huh")
            if self.__connection.is_established():
                await self.__connection.ping()
            await asyncio.sleep(1)

    async def connect(self) -> None:
        print("Connecting asynchronously...")

        connection = Connection()
        await connection.connect()
        if connection.is_established():
            print("Connected")
        else:
            raise RuntimeError("Failed to connect to the websocket server")

        await connection.send_init()

    async def on_move(self) -> None:
        if self.__online:
            if not self.__connection.is_established():
                await self.__connection.connect()
            move: PieceMove = self.__game.get_last_move()
            print("On move")
            print(move.to_dict())
            await self.__connection.send_move(move.to_dict())
