from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import PieceModel
from game.piece.movement import Movement, PieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class RangedPieceMovement(PieceMovement):
    def __init__(self, bishop: Piece, board: Board) -> None:
        super().__init__(bishop, board)
        self._movements: list[tuple[Movement, Vector2d]] = []
        
    @property
    def movements(self) -> list[tuple[Movement, Vector2d]]:
        return self._movements

    # override
    def get_all_moves(self) -> list[list[Vector2d]]:
        moves: list[list[Vector2d]] = []
        p = self._piece

        for movement, delta in self.movements:
            moves.append(self.iterate_squares(p.position + delta, movement)[0])

        return moves

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        self._legal_moves.clear()
        p = self._piece
        b = self._board

        for moves in self.get_all_moves():
            if len(moves) <= 0:
                continue

            last_move = moves[len(moves) - 1]
            if b.is_piece_at(last_move) and b.get_piece(last_move).is_same_color(p):
                moves.pop()
            self._legal_moves.append(moves)

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
        Check squares of the board and return moves list and possible blocking piece (p). If the player's piece is
        the last one in iteration, that square is included in returned list.

        :param origin: origin vector of ray checking
        :param movement: movement type of piece (rank, file, diagonal)

        :return: tuple of list of moves and optional piece, if is in the way of the ray
        """

        # Aliases
        b = self._board
        piece = self._piece

        moves: list[Vector2d] = []
        pieces: list[Piece] = []
        squares = Movement.get_squares(movement, b, origin)

        for v in squares:
            p = b.get_piece(v)

            #
            # Add position v, if square is empty
            #
            if b.can_move_to(v, piece) and len(pieces) == 0:
                moves.append(v)
            #
            #
            #
            elif b.can_move_to(v, piece, capture=True):
                if len(pieces) == 0:
                    moves.append(v)
                if p:
                    pieces.append(p)
            #
            # Add position v, if the player's piece is on the square
            #
            elif p and piece.is_same_color(p):
                moves.append(v)
                return moves, pieces

        return moves, pieces
