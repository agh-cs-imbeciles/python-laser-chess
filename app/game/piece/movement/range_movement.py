from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import PieceModel
from game.piece.movement import Movement, PieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece
    from game.piece.movement import Movement


class RangePieceMovement(PieceMovement):
    def __init__(self, bishop: Piece, board: Board) -> None:
        super().__init__(bishop, board)
        self._movements: list[tuple[Movement, Vector2d]] = []
        
    @property
    def movements(self) -> list[tuple[Movement, Vector2d]]:
        return self._movements

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        self._legal_moves.clear()
        p = self._piece

        for movement, delta in self._movements:
            self._legal_moves.append(self.iterate_squares(p.position + delta, movement)[0])

        return self._legal_moves

    # override
    def get_pinned_piece(self) -> Piece | None:
        p = self._piece

        for movement, delta in self._movements:
            pieces = self.iterate_squares(p.position + delta, movement)[1]
            if len(pieces) >= 2 and pieces[1].model == PieceModel.KING:
                return pieces[0]

        return None

    def iterate_squares(self, origin: Vector2d, movement: Movement) -> tuple[list[Vector2d], list[Piece]]:
        """
        Check squares of the board and return legal moves (lm) list and possible blocking piece (p).
        :param origin: origin vector of ray checking
        :param movement: movement type of piece (rank, file, diagonal)
        :return: tuple of legal moves and optional piece, if is in the way of the ray
        """

        # Aliases
        b = self._board
        piece = self._piece

        legal_moves: list[Vector2d] = []
        pieces: list[Piece] = []
        squares = Movement.get_squares(movement, b, origin)

        for v in squares:
            p = b.get_piece(v)

            if b.can_move_to(v, piece) and len(pieces) == 0:
                legal_moves.append(v)
            elif b.can_move_to(v, piece, capture=True):
                if len(pieces) == 0:
                    legal_moves.append(v)
                pieces.append(b.get_piece(v))
            elif p and piece.player_id == p.player_id:
                return legal_moves, pieces

        return legal_moves, pieces
