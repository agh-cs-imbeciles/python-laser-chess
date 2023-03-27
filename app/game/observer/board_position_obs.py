from abc import ABC, abstractmethod
from utils import Vector2d
from game.observer import PositionObserver


class PositionObserver(ABC, PositionObserver):
    # override PositionObserver
    @abstractmethod
    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        pass
