from __future__ import annotations
from abc import ABC, abstractmethod
from utils import Vector2d
from game.pieces import Piece


class BoardPositionObserver(ABC):
    # override PositionObserver
    @abstractmethod
    def on_position_change(self, origin: Vector2d, destination: Vector2d, capturedPiece: Piece | None = None) -> None:
        pass
