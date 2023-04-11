from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece.movement import Movement, PieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece
    from game.piece.movement import Movement


class RangePieceMovement(PieceMovement):
    def __init__(self, bishop: Piece, board: Board) -> None:
        super().__init__(bishop, board)

    @abstractmethod
    def get_legal_moves(self) -> list[list[Vector2d]]:
        pass

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

        found_player_piece = False
        legal_moves: list[Vector2d] = []
        pieces: list[Piece] = []
        squares = Movement.get_squares(movement, b, origin)

        for v in squares:
            p = b.get_piece(v)

            if b.can_move_to(v, piece) and len(pieces) == 0 and not found_player_piece:
                legal_moves.append(v)
            elif p and piece.player_id != p.player_id and not found_player_piece:
                if len(pieces) == 0:
                    legal_moves.append(v)
                pieces.append(b.get_piece(v))
            elif p and piece.player_id == p.player_id:
                found_player_piece = True

        return legal_moves, pieces
