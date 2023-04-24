from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import Piece, PieceModel
from game.piece.movement import PieceMovement

if TYPE_CHECKING:
    from game import Board


class PawnMovement(PieceMovement):
    def __init__(
        self,
        pawn: Piece,
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
        
    @property
    def direction(self):
        return self._direction

    #override
    def get_all_moves(self) -> list[list[Vector2d]]:
        moves: list[list[Vector2d]] = [[]]

        # Aliases
        b = self._board
        p = self._piece
        dir = self._direction
        enp = self._en_passant_position

        p_left = p.position - dir.reverse_axis() + dir  # Left capture position
        p_right = p.position + dir.reverse_axis() + dir  # Right capture position

        #
        # Advance 1 square (default move)
        #
        if b.can_move_to(p.position + dir, self._piece):
            moves[0].append(p.position + dir)
        #
        # Advance 2 squares (first move)
        #
        if (
            p.position == self._initial_position
            and b.can_move_to(p.position + dir.multiply_scalar(2), self._piece)
            and len(moves[0]) > 0
        ):
            moves[0].append(p.position + dir.multiply_scalar(2))
        #
        # Capture a piece
        #
        for pos in [p_left, p_right]:
            if not b.is_out_of_bounds(pos):
                moves[0].append(pos)
        #
        # En passant
        #
        if 0 < enp.x == p.position.x or 0 < enp.y == p.position.y:
            for pos in [p_left, p_right]:
                p0, mvmt = b.get_piece(pos - dir), b.get_piece_movement(pos - dir)
                if p0 and p0.is_same_color(p) and p0.model == PieceModel.PAWN and b.can_move_to(pos, self._piece):
                    self._legal_moves[0].append(pos)

        return moves

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        # Clear legal moves
        self._legal_moves.clear()
        self._legal_moves.append([])

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
        advance_1 = False
        if b.can_move_to(p.position + dir, self._piece):
            self._legal_moves[0].append(p.position + dir)
            advance_1 = True
        #
        # Advance 2 squares (first move)
        #
        if p.position == self._initial_position and b.can_move_to(p.position + dir.multiply_scalar(2), self._piece) and advance_1:
            self._legal_moves[0].append(p.position + dir.multiply_scalar(2))
        #
        # Capture a piece
        #
        for pos in [p_left, p_right]:
            if b.can_move_to(pos, self._piece, capture_required=True):
                self._legal_moves[0].append(pos)
        #
        # En passant
        #
        if 0 < enp.x == p.position.x or 0 < enp.y == p.position.y:
            for pos in [p_left, p_right]:
                p0, mvmt = b.get_piece(pos - dir), b.get_piece_movement(pos - dir)
                if p0 and not p0.is_same_color(p) and p0.model == PieceModel.PAWN and b.can_move_to(pos, self._piece):
                    self._legal_moves[0].append(pos)

        return self._legal_moves
