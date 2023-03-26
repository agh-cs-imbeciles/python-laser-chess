from game.pieces.piece import Piece
from game.pieces.move.piece_move_type import PieceMoveType
from game.board import Board
from utils.vector2d import Vector2d


class PieceMoveDetector:
    @staticmethod
    def detect(board: Board, piece: Piece, to: Vector2d) -> PieceMoveType:
        pass
