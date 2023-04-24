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

    @abstractmethod
    def get_all_moves(self) -> list[list[Vector2d]]:
        """
        Get all possible moves, which are legal or any piece is on the square
        and if it's enemy's, it must be capturable.\n
        For example,
        ranged pieces' list of moves ends on a first occurred piece (including) or boundary of the chessboard.
        :return: List of lists containing all possible moves.
        """
        pass

    @abstractmethod
    def get_legal_moves(self) -> list[list[Vector2d]]:
        pass

    def get_pinned_piece(self) -> Piece | None:
        return None
