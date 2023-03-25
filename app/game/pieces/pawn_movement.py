from piece_movement import PieceMovement
# from piece import Piece
# from piece_model import PieceModel
# from game.board import Board
# from utils.vector2d import Vector2d


class PawnMovement(PieceMovement):
    def __init__(self, pawn, board):
        super().__init__(pawn, board)
        print(self._piece, self._board)

    # override
    def get_legal_moves(self):
        pass
