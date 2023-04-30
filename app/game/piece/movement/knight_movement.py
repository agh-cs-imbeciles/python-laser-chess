from __future__ import annotations
from typing import TYPE_CHECKING
from game.piece.movement import PieceMovement
from utils import BoardVector2d, Symmetry

if TYPE_CHECKING:
    from game.piece.piece import Piece
    from game.board import Board


class KnightMovement(PieceMovement):
    def __init__(self, knight: Piece, board: Board) -> None:
        super().__init__(knight, board)

    # override
    def get_all_moves(self) -> list[list[BoardVector2d]]:
        moves: list[[BoardVector2d]] = [[]]

        base_vectors = [BoardVector2d(1, 2), BoardVector2d(2, 1)]
        pos = self._piece.position
        symmetries = [None, Symmetry.X_AXIS, Symmetry.ORIGIN, Symmetry.Y_AXIS]
        positions = [pos + v.pivot_symmetry(s) if s is not None else pos + v for v in base_vectors for s in symmetries]

        for p in positions:
            if not self._board.is_out_of_bounds(p):
                moves[0].append(p)

        return moves

    # override
    def get_legal_moves(self) -> list[list[BoardVector2d]]:
        self._legal_moves.clear()
        self._legal_moves.append([])

        for m in self.get_all_moves()[0]:
            if self._board.can_move_to(m, self._piece, capture=True):
                self._legal_moves[0].append(m)

        return self._legal_moves

