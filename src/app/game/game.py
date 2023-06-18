from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio

from app.game import GameTimer
from app.client import Connection

if TYPE_CHECKING:
    from game import Game
    from game.piece.move import PieceMove


class GameApplication:
    def __init__(self, game: Game, **kwargs) -> None:
        self.__game = game
        self.__online = kwargs.get("online", False)
        self.__player_id: str | None = None

        # Create timer
        seconds_per_player: int = 5 * 60
        player_number: int = 2
        self.__game_timer: GameTimer = GameTimer(self.__game, seconds_per_player, player_number)
        self.__game_timer.run()

        if self.__online:
            # Establish connection with the websockets server
            asyncio.run(self.establish_connection())

    async def establish_connection(self):
        response: dict[str, any] = await Connection.communicate_init()
        self.__player_id = response.get("playerId")
        print(self.__player_id)

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
            await Connection.communicate_move(move.to_dict(), self.__player_id)
