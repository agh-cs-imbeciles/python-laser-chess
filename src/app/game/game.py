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
            asyncio.run(Connection.send_init())

    # async def __init_connection(self):
    #     self.__connection = Connection()
    #     await self.__connection.connect()
    #     await Connection.send_init()

    def on_move(self) -> None:
        if self.__online:
            # print(self.__game.get_last_move().to_dict())
            # asyncio.run(Sender.send_move(self.__game.get_last_move().to_dict()))
            move: PieceMove = self.__game.get_last_move()
            asyncio.run(Connection.send_move(move.to_dict()))
