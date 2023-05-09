from __future__ import annotations
from abc import ABC, abstractmethod
from utils import BoardVector2d
from game.piece import Piece


class BoardPositionObserver(ABC):
    # override PositionObserver
    @abstractmethod
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d, captured_piece: Piece | None = None) -> None:
        pass
