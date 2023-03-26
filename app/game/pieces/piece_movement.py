from abc import ABC, abstractmethod
from game.game import Board
from game.pieces.piece import Piece

class PieceMovement(ABC):
    def __init__(self, piece: Piece, board: Board):
        self._piece = piece
        self._board = board
        self._legal_moves = []

    @abstractmethod
    def get_legal_moves(self):
        pass
