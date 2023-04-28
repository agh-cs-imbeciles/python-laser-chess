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
            moves.append(self.iterate_squares(p.position + delta, movement))

        return moves

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        self._legal_moves.clear()

        # Aliases
        p, b = self._get_aliases()

        for moves in self.get_all_moves():
            if len(moves) <= 0:
                continue

            moves_row = []
            for i, position in enumerate(moves):
                _p = b.get_piece(position)
                if _p and _p.is_same_color(): break
                moves_row.append(position)
                if _p and not _p.is_same_color(): break

            if len(moves_row) > 0:
                self._legal_moves.append(moves_row)

        return self._legal_moves

    # override
    def get_capturable_moves(self) -> list[list[Vector2d]]:
        pass

    # override
    # def get_pinned_piece(self) -> Piece | None:
    #     p = self._piece
    #
    #     for movement, delta in self._movements:
    #         pieces = self.iterate_squares(p.position + delta, movement)[1]
    #         if len(pieces) >= 2 and pieces[1].model == PieceModel.KING:
    #             return pieces[0]
    #
    #     return None

    def iterate_squares(self, origin: Vector2d, movement: Movement) -> list[Vector2d]:
        """
        Iterate through every square of the board, based on passed argument movement and return list of moves.

        :param origin: origin vector of ray checking
        :param movement: movement type of piece (rank, file, diagonal)

        :return: List of moves
        """

        # Aliases
        p, b = self._get_aliases()

        moves: list[Vector2d] = []
        squares = Movement.get_squares(movement, b, origin)

        for sqr in squares:
            #
            # Add position sqr, if square is not out of bounds
            #
            if not b.is_out_of_bounds(sqr):
                moves.append(sqr)

        return moves
