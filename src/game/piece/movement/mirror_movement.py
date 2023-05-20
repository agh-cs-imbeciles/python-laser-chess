from __future__ import annotations
from typing import TYPE_CHECKING
from utils import BoardVector2d
from game.piece import Piece
from game.piece.movement import PieceMovement


if TYPE_CHECKING:
    from game import Board


class MirrorMovement(PieceMovement):
    def __init__(
            self,
            mirror: Piece,
            board: Board,
    ) -> None:
        super().__init__(mirror, board)
        self._initial_position: BoardVector2d = mirror.position.copy()

    def get_all_moves(self) -> list[list[BoardVector2d]]:
        p, b = self._get_aliases()
        moves = [[]]

        deltas = filter(lambda x: x != BoardVector2d(0, 0),
                        [BoardVector2d(x, y) for y in range(-1, 2) for x in range(-1, 2)])
        for d in deltas:
            if not b.is_out_of_bounds(p.position + d):
                moves[0].append(p.position + d)

        return moves

    def get_legal_moves(self) -> list[list[BoardVector2d]]:
        # Clear legal moves
        self._legal_moves.clear()
        self._legal_moves.append([])

        # Aliases
        p, b = self._get_aliases()

        for m in self.get_all_moves()[0]:
            if b.can_move_to(m, p, capture=False):
                self._legal_moves[0].append(m)

        return self._legal_moves

