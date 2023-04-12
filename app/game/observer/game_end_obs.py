from __future__ import annotations
from abc import ABC, abstractmethod
from utils import Vector2d
from game.piece import Piece
from game.piece.move import PieceMoveType


class GameEndObserver(ABC):
    # override PositionObserver
    @abstractmethod
    def on_end(self, winner: int, type: PieceMoveType) -> None:
        pass
