from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from common import MessageStatus
from app.game import GameTimer
from app.client import Connection

if TYPE_CHECKING:
    from game import Game
    from game.piece.move import PieceMove


class GameApplication:
    def __init__(self, game: Game, **kwargs) -> None:
        self.__game = game

        # Online gameplay properties
        self.__online: bool = kwargs.get("online", False)
        self.__game_id: str | None = kwargs.get("game_id")
        self.__player_id: str | None = kwargs.get("player_id")

        # Create timer
        seconds_per_player: int = 5 * 60
        player_number: int = 2
        self.__game_timer: GameTimer = GameTimer(self.__game, seconds_per_player, player_number)
        self.__game_timer.run()

    async def on_move(self) -> None:
        if self.__online:
            move: PieceMove = self.__game.get_last_move()
            await Connection.communicate_move(move.to_dict(), self.__player_id)


class PreGameHelper:
    @classmethod
    async def create_game(cls) -> tuple[str, str]:
        print("Creating the new game...")

        response: dict[str, any] = await Connection.create_game()
        status_raw: str | None = response.get("status")
        if not status_raw:
            raise RuntimeError("Failed creating the new game, message status hasn't been sent")
        status: MessageStatus = MessageStatus.from_str(status_raw)
        if status == MessageStatus.ERROR:
            raise RuntimeError("Failed creating the new game, error message status")

        game_id: str | None = response.get("gameId")
        if not game_id:
            raise RuntimeError("Failed creating the new game, game ID hasn't been sent")
        player_id: str | None = response.get("playerId")
        if not player_id:
            raise RuntimeError("Failed creating the new game, player ID hasn't been sent")

        print("Succeed creating the new game")

        return game_id, player_id

    @classmethod
    async def wait_for_other_player(cls) -> None:
        print("Waiting for the other player to join...")
        await Connection.wait_for_player()
        print("Succeed waiting for the other player")

    @classmethod
    async def join_game(cls, game_id: str) -> str:
        print("Joining the game...")

        response: dict[str, any] = await Connection.join_game(game_id)
        status_raw: str | None = response.get("status")
        if not status_raw:
            raise RuntimeError("Failed joining the game, message status hasn't been sent")
        status: MessageStatus = MessageStatus.from_str(status_raw)
        if status == MessageStatus.ERROR:
            raise RuntimeError("Failed joining the game, error message status")

        player_id: str | None = response.get("playerId")
        if not player_id:
            raise RuntimeError("Failed joining the game, player ID hasn't been sent")

        print("Succeed joining the game")

        return player_id
