from utils import Vector2d
import game as g
import game.pieces as pcs
import game.pieces.move as mv


class PieceMoveDetector:
    @staticmethod
    def detect(board: g.Board, piece: pcs.Piece, to: Vector2d) -> mv.PieceMoveType:
        pass
