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
            self.direction.reverse_axis() + self.direction,    # Left capture delta
            self.direction.reverse_axis() + self.direction     # Right capture delta
        ]
        
    @property
    def direction(self) -> Vector2d:
        return self._direction

    @property
    def capture_deltas(self) -> list[Vector2d]:
        return self._capture_deltas

    def __is_en_passant_legal(self, destination: Vector2d) -> bool:
        p, b = self._piece, self._board
        other = b.get_piece(destination - self.direction)
        return other and not other.is_same_color(p) and other.model == PieceModel.PAWN and b.can_move_to(destination, p)

    #override
    def get_all_moves(self) -> list[list[Vector2d]]:
        moves: list[list[Vector2d]] = [[]]

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
        for pos in [p.position + d for d in self.capture_deltas]:
            if not b.is_out_of_bounds(pos):
                moves[0].append(pos)
        #
        # En passant
        #
        if p.position == enp:
            for pos in [p.position + d for d in self.capture_deltas]:
                p0, _ = b.get_piece(pos - dir), b.get_piece_movement(pos - dir)
                if self.__is_en_passant_legal(pos):
                    if pos not in moves[0]:
                        moves[0].append(pos)

        return moves

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        # Clear legal moves
        self._legal_moves.clear()
        self._legal_moves.append([])

        # Aliases
        b = self._board
        p = self._piece
        enp = self._en_passant_position

        moves = self.get_all_moves()

        capture_moves = [p.position + d for d in self.capture_deltas]
        for m in moves[0]:
            #
            # Capture
            #
            if m in capture_moves and p.position != enp and not b.can_move_to(m, p, capture_required=True):
                continue
            #
            # En passant
            #
            if m in capture_moves and p.position == enp and not self.__is_en_passant_legal(m):
                continue

            self._legal_moves[0].append(m)

        return self._legal_moves
