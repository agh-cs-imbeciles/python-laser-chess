from __future__ import annotations
from typing import TYPE_CHECKING
from copy import deepcopy
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
        self._capture_deltas: list[Vector2d] = [
            -self.direction.reverse_axis() + self.direction,    # Left capture delta
            self.direction.reverse_axis() + self.direction      # Right capture delta
        ]
        
    @property
    def direction(self) -> Vector2d:
        return self._direction

    @property
    def capture_deltas(self) -> list[Vector2d]:
        return self._capture_deltas

    @property
    def promotion_position(self):
        return self._promotion_position

    def __is_en_passant_legal(self, destination: Vector2d) -> bool:
        p, b = self._get_aliases()
        other = b.get_piece(destination - self.direction)
        return other and not other.is_same_color(p) and other.model == PieceModel.PAWN and b.can_move_to(destination, p)

    # override
    def get_all_moves(self) -> list[list[Vector2d]]:
        moves: list[list[Vector2d]] = [[]]

        # Aliases
        p, b = self._get_aliases()
        dir = self.direction
        enp = self._en_passant_position

        #
        # Advance 1 square (default move)
        #
        if not b.is_out_of_bounds(p.position + dir):
            moves[0].append(p.position + dir)
        #
        # Advance 2 squares (first move)
        #
        if not b.is_out_of_bounds(p.position + dir.multiply_scalar(2)):
            moves[0].append(p.position + dir.multiply_scalar(2))
        #
        # Capture
        #
        for pos in self.get_capturable_moves()[0]:
            if not b.is_out_of_bounds(pos):
                moves[0].append(pos)
        #
        # En passant
        #
        if p.position != enp:
            return moves
        for pos in [p.position + d for d in self.capture_deltas]:
            if self.__is_en_passant_legal(pos):
                moves[0].append(pos)

        return moves

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        # Clear legal moves
        self._legal_moves.clear()
        self._legal_moves.append([])

        # Aliases
        p, b = self._get_aliases()
        dir = self.direction
        enp = self._en_passant_position

        moves = []

        #
        # Advance 1 square (default move)
        #
        if b.can_move_to(p.position + dir, self._piece):
            moves.append(p.position + dir)
        #
        # Advance 2 squares (first move)
        #
        if (
                not p.moved()
                and b.can_move_to(p.position + dir.multiply_scalar(2), self._piece)
                and len(moves) > 0
        ):
            moves.append(p.position + dir.multiply_scalar(2))
        #
        # Capture
        #
        for m in self.get_capturable_moves()[0]:
            if b.can_move_to(m, p, capture_required=True):
                moves.append(m)
        #
        # En passant
        #
        if p.position != enp:
            self._legal_moves.append(moves)
            return self._legal_moves
        for pos in [p.position + d for d in self.capture_deltas]:
            if self.__is_en_passant_legal(pos):
                moves.append(pos)

        self._legal_moves.append(moves)
        return self._legal_moves

    # override
    def get_capturable_moves(self) -> list[list[Vector2d]]:
        p, b = self._get_aliases()
        capture_positions = [p.position + d for d in self._capture_deltas]

        return [capture_positions]
