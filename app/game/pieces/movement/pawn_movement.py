from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.pieces import Piece, PieceModel
from game.pieces.movement import PieceMovement

if TYPE_CHECKING:
    from game import Board


class PawnMovement(PieceMovement):
    def __init__(
        self, pawn: Piece,
        board: Board,
        direction: Vector2d,
        en_passant_position: Vector2d,
        promotion_position: Vector2d
    ) -> None:
        super().__init__(pawn, board)
        self._initial_position: Vector2d = pawn.position.copy()
        self._direction: Vector2d = direction
        self._en_passant_position: Vector2d = en_passant_position
        self._promotion_position: Vector2d = promotion_position

    # override
    def get_legal_moves(self) -> list[Vector2d]:
        # Clear legal moves
        self._legal_moves.clear()

        # Aliases
        b = self._board
        p = self._piece
        dir = self._direction
        enp = self._en_passant_position

        p_left = p.position - dir.reverse_axis() + dir      # Left capture position
        p_right = p.position + dir.reverse_axis() + dir     # Right capture position

        #
        # Advance 1 square (default move)
        #
        if b.can_move_to(p.position + dir):
            self._legal_moves.append(p.position + dir)
        #
        # Advance 2 squares (first move)
        #
        if p.position == self._initial_position and b.can_move_to(p.position + dir.multiply_scalar(2)):
            self._legal_moves.append(p.position + dir.multiply_scalar(2))
        #
        # Capture a piece
        #
        for pos in [p_left, p_right]:
            if b.get_piece(pos) and b.get_piece(pos).player_id != p.player_id:
                self._legal_moves.append(pos)
        #
        # En passant
        #
        if 0 < enp.x == p.position.x or 0 < enp.y == p.position.y:
            for pos in [p_left, p_right]:
                p0 = b.get_piece(pos - dir)
                if p0 and p0.player_id != p.player_id and p0.model == PieceModel.PAWN and b.can_move_to(pos):
                    self._legal_moves.append(pos)

        return self._legal_moves
