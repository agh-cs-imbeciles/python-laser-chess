from abc import ABC, abstractmethod
from game.board import Board
from game.pieces.piece import Piece
from utils.vector2d import Vector2d


class PieceMovement(ABC):
    def __init__(self, piece: Piece, board: Board) -> None:
        self._piece: Piece = piece
        self._board: Board = board
        self._legal_moves: list[Vector2d] = []

    @abstractmethod
    def get_legal_moves(self) -> list[Vector2d]:
        pass
