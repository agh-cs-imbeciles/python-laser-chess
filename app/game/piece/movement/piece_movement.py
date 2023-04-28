from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from utils import Vector2d

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class PieceMovement(ABC):
    def __init__(self, piece: Piece, board: Board) -> None:
        self._piece: Piece = piece
        self._board: Board = board
        self._legal_moves: list[list[Vector2d]] = []

    def _get_aliases(self) -> tuple[Piece, Board]:
        return self._piece, self._board

    @abstractmethod
    def get_all_moves(self) -> list[list[Vector2d]]:
        """
        Get all available moves, excluding out of bounds ones.

        :return: List of lists containing all possible moves.
        """
        pass

    @abstractmethod
    def get_legal_moves(self) -> list[list[Vector2d]]:
        """
        Get moves only that are legal - that's mean, player is able move the piece on a square
        without violating the rules.

        :return: List of lists containing all legal moves.
        """
        pass

    @abstractmethod
    def get_capturable_moves(self) -> list[list[Vector2d]]:
        """
        Get moves only that are potentially capturable, excluding out of bound ones.

        Examples
        ========
        Pawns only have left and right upper squares, counted as capturable (without en passant).
        Ranged pieces have whole lines, counted as capturable.

        :return: List of lists containing all moves described above.
        """

    # def get_pinned_piece(self) -> Piece | None:
    #     return None
