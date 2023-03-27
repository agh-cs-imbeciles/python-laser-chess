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

    def check_squares(
        self, piece: Piece, board, origin: Vector2d, destination: Vector2d, increment: Tuple[int, int]
    ) -> None:
        if increment[0] == 0 and increment[1] == 0:
            return

        if increment[0] == 0:
            dys = [dy for dy in range(origin.y, destination.y, increment[1])]
            dxs = [origin.x for _ in dys]
        else:
            dxs = [dx for dx in range(origin.x, destination.x, increment[0])]
            dys = [origin.y for _ in dxs]

        deltas = zip(dxs, dys)
        for dx, dy in deltas:
            pos = Vector2d(piece.position.x + dy, piece.position.y + dx)
            if not board.can_move_to(pos, piece):
                break
            self._legal_moves.append(pos)
