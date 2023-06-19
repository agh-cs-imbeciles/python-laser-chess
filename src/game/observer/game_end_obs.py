from __future__ import annotations
from abc import ABC, abstractmethod
from utils import BoardVector2d, GameEnding


class GameEndObserver(ABC):
    # override PositionObserver
    @abstractmethod
    def on_end(self, winner: int, game_ending: GameEnding) -> None:
        pass
