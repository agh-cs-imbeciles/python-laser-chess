from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import Piece, PieceModel
from game.piece.movement import PieceMovement

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
            p = self._piece.position + d
            if self._board.can_move_to(p, self._piece) and not self._board.checked_squares[self._piece.player_id].get(p):
                self._legal_moves.append(p)

        #
        # Castling
        #
        if not self._piece.moved():
            y: int = self._piece.position.y

            #
            # Queen-side castling
            #
            queen_side_rook: Piece | None = self._board.get_piece(Vector2d(0, y))
            if queen_side_rook and queen_side_rook.model == PieceModel.ROOK and not queen_side_rook.moved():
                self._legal_moves.append(self._piece.position + Vector2d(-2, 0))
            #
            # King-side castling
            #
            king_side_rook: Piece | None = self._board.get_piece(Vector2d(self._board.width - 1, y))
            if king_side_rook and king_side_rook.model == PieceModel.ROOK and not king_side_rook.moved():
                self._legal_moves.append(self._piece.position + Vector2d(2, 0))

        return self._legal_moves
