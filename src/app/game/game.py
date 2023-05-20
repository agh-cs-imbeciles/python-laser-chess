from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio
from app.client import Sender

if TYPE_CHECKING:
    from game import Game


class GameApplication:
    def __init__(self, game: Game) -> None:
        self._game = game

    def on_move(self) -> None:
        print(self._game.get_last_move().to_dict())
        asyncio.run(Sender.send_move(self._game.get_last_move().to_dict()))
