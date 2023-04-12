from __future__ import annotations
from abc import ABC, abstractmethod
from utils import Vector2d
from game.piece import Piece


class BoardPositionObserver(ABC):
    # override PositionObserver
    @abstractmethod
    def on_position_change(self, origin: Vector2d, destination: Vector2d, captured_piece: Piece | None = None) -> None:
        pass
