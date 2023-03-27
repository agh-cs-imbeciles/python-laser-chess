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

        if increment[0] != 0:
            xs = [x for x in range(origin.x, destination.x, increment[0])]
        if increment[1] != 0:
            ys = [y for y in range(origin.y, destination.y, increment[1])]
        if increment[0] == 0:
            xs = [origin.x for _ in ys]
        if increment[1] == 0:
            ys = [origin.y for _ in xs]

        deltas = zip(xs, ys)
        for x, y in deltas:
            pos = Vector2d(x, y)
            if not board.can_move_to(pos):
                if board.is_piece_at(pos) and piece.player_id != board.get_piece(pos).player_id:
                    self._legal_moves.append(pos)
                break
            self._legal_moves.append(pos)
