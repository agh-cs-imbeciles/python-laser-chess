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
        self.__loop = asyncio.get_event_loop()

        if self.__online:
            asyncio.run(self.establish_connection())

    async def establish_connection(self):
        await Connection.send_init()

    # async def run_async(self) -> None:
    #     await self.connect()
    #     while True:
    #         print("huh1")
    #         if self.__connection.is_established():
    #             await self.__connection.ping()
    #         await asyncio.sleep(1)
    #
    # async def connect(self) -> None:
    #     print("Connecting asynchronously...")
    #
    #     connection = Connection()
    #     await connection.connect()
    #     if connection.is_established():
    #         print("Connected")
    #     else:
    #         raise RuntimeError("Failed to connect to the websocket server")
    #
    #     await connection.send_init()

    async def on_move(self) -> None:
        if self.__online:
            move: PieceMove = self.__game.get_last_move()
            await Connection.send_move(move.to_dict())
