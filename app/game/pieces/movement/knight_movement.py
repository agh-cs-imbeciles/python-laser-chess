from __future__ import annotations
from typing import TYPE_CHECKING
from game.pieces.movement import PieceMovement
from utils.vector2d import Vector2d

if TYPE_CHECKING:
    from game.pieces.piece import Piece
    from game.board import Board
    from utils.vector2d import Vector2d


class KnightMovement(PieceMovement):
    def __init__(self, pawn: Piece, board: Board) -> None:
        super().__init__(pawn, board)

    # override
    def get_legal_moves(self) -> list[Vector2d]:
        self._legal_moves.clear()
        base_vectors = (Vector2d(1, 2),Vector2d(2, 1))
        p = self._piece
        ftn = [False, True, None]
        for j in ftn:
            for k in base_vectors:
                v = p.position + k.pivot_symmetry(j)
                if self._board.can_move_to(v, self._piece):
                    self._legal_moves.append(v)
        v = p.position + base_vectors[0].multiply_scalar(-1)
        if self._board.can_move_to(v, self._piece):
            self._legal_moves.append(v)
        v = p.position + base_vectors[1].multiply_scalar(-1)
        if self._board.can_move_to(v, self._piece):
            self._legal_moves.append(v)
        return self._legal_moves
