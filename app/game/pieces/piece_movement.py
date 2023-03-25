from abc import ABC, abstractmethod


class PieceMovement(ABC):
    def __init__(self, piece, board):
        self._piece = piece
        self._board = board

    @abstractmethod
    def get_legal_moves(self):
        pass
