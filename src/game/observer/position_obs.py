from abc import ABC, abstractmethod

from app.gui.utils import Paths
from utils import BoardVector2d


class PositionObserver(ABC):
    @abstractmethod
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        pass
    @abstractmethod
    def on_rotation(self, origin: BoardVector2d, rotation: Paths) -> None:
        pass
