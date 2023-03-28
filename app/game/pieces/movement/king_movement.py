from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.pieces import Piece, PieceModel
from game.pieces.movement import PieceMovement

if TYPE_CHECKING:
    from game import Board


class KingMovement(PieceMovement):
    def __init__(self, king: Piece, board: Board) -> None:
        super().__init__(king, board)
        self._initial_position: Vector2d = king.position.copy()

    # override
    def get_legal_moves(self) -> list[Vector2d]:
        # Clear legal moves
        self._legal_moves.clear()

        deltas = filter(lambda x: x != Vector2d(0, 0), [Vector2d(x, y) for y in range(-1, 2) for x in range(-1, 2)])
        for d in deltas:
            if self._board.can_move_to(self._piece.position + d, self._piece):
                self._legal_moves.append(self._piece.position + d)

        return self._legal_moves

    # override
    def get_all_obstructing_pieces(self) -> list[Piece]:
        return []
