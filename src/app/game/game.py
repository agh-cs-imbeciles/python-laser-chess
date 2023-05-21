from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio
from app.client import Sender
from app.config import GameSettings

if TYPE_CHECKING:
    from game import Game


class GameApplication:
    def __init__(self, game: Game) -> None:
        self._game = game
        self.__settings = GameSettings(False)

    def on_move(self) -> None:
        if self.__settings.online_gameplay:
            print(self._game.get_last_move().to_dict())
            asyncio.run(Sender.send_move(self._game.get_last_move().to_dict()))
