from abc import ABC, abstractmethod
from utils import BoardVector2d, Rotation


class PositionObserver(ABC):
    @abstractmethod
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        pass

    @abstractmethod
    def on_rotation(self, origin: BoardVector2d, rotation: Rotation) -> None:
        pass
