from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple
from utils import Vector2d

if TYPE_CHECKING:
    from game.pieces import Piece


class PieceMovement(ABC):
    def __init__(self, piece: Piece, board) -> None:
        self._piece: Piece = piece
        self._board = board
        self._legal_moves: list[Vector2d] = []

    @abstractmethod
    def get_legal_moves(self) -> list[Vector2d]:
        pass
