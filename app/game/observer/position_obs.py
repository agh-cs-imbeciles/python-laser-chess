from abc import ABC, abstractmethod
from utils import BoardVector2d


class PositionObserver(ABC):
    @abstractmethod
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        pass
