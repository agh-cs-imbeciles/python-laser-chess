from abc import ABC, abstractmethod
from utils import Vector2d


class PositionObserver(ABC):
    @abstractmethod
    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        pass
