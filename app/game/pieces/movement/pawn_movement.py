from __future__ import annotations
from utils import Vector2d
import game as g
import game.pieces as pcs
import game.pieces.movement as mvm


class PawnMovement(mvm.PieceMovement):
    def __init__(
        self, pawn: pcs.Piece,
        board: g.Board,
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
        self._legal_moves.clear()
        b = self._board
        p = self._piece
        dir = self._direction

        #
        # Advance 1 square (default move)
        #
        if b.can_move_to(p.position + dir, p):
            self._legal_moves.append(p.position + dir)
        #
        # Advance 2 squares (first move)
        #
        if p.position == self._initial_position and b.can_move_to(p.position + dir.multiply_scalar(2), p):
            self._legal_moves.append(p.position + dir.multiply_scalar(2))
        #
        # En passant
        #
        if p.position == self._en_passant_position:
            #
            # En passant (left)
            #
            if b.get_piece(p.position - dir.reverse_axis()) and b.can_move_to(p.position - dir.reverse_axis()):
                self._legal_moves.append(p.position - dir.reverse_axis())
            #
            # En passant (right)
            #
            if b.get_piece(p.position + dir.reverse_axis()) and b.can_move_to(p.position + dir.reverse_axis()):
                self._legal_moves.append(p.position + dir.reverse_axis())

        return self._legal_moves
