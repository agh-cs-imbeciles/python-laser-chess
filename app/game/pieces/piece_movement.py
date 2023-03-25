from abc import ABC, abstractmethod


class PieceMovement(ABC):
    def __init__(self, piece, board):
        self._piece = piece
        self._board = board
        self._legal_moves = []

    @abstractmethod
    def get_legal_moves(self):
        pass
