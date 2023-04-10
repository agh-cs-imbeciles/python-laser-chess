from __future__ import annotations
from typing import TYPE_CHECKING
from game.piece.movement import PieceMovement
from utils.vector2d import Vector2d, Symmetry

if TYPE_CHECKING:
    from game.piece.piece import Piece
    from game.board import Board
    from utils.vector2d import Vector2d


class KnightMovement(PieceMovement):
    def __init__(self, knight: Piece, board: Board) -> None:
        super().__init__(knight, board)

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        self._legal_moves.clear()
        self._legal_moves.append([])

        base_vectors = [Vector2d(1, 2), Vector2d(2, 1)]
        pos = self._piece.position
        symmetries = [None, Symmetry.X_AXIS, Symmetry.ORIGIN, Symmetry.Y_AXIS]
        positions = [pos + v.pivot_symmetry(s) if s is not None else pos + v for v in base_vectors for s in symmetries]

        for p in positions:
            if self._board.can_move_to(p, self._piece, True):
                self._legal_moves[0].append(p)

        return self._legal_moves
