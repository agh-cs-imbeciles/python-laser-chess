from typing import Tuple
from piece_movement import PieceMovement
from game.pieces.piece import Piece
from game.board import Board
from utils.vector2d import Vector2d


class BishopMovement(PieceMovement):
    def __init__(self, pawn: Piece, board: Board) -> None:
        super().__init__(pawn, board)

    # override
    def get_legal_moves(self) -> list[Vector2d]:
        self._legal_moves.clear()
        b = self._board
        p = self._piece

        def check_diagonal(origin: Vector2d, destination: Vector2d, increment: Tuple[int, int]):
            deltas = zip(
                [dx for dx in range(origin.x, destination.x, increment[0])],
                [dy for dy in range(origin.y, destination.y, increment[1])]
            )
            for dx, dy in deltas:
                pos = Vector2d(p.position.x + dy, p.position.y + dx)
                if not b.can_move_to(pos, p):
                    break
                self._legal_moves.append(pos)

        #
        # Upper right diagonal
        #
        check_diagonal(p.position + Vector2d(1, 1), Vector2d(b.width, b.height), (1, 1))
        #
        # Bottom left diagonal
        #
        check_diagonal(p.position + Vector2d(-1, -1), Vector2d(-1, -1), (-1, -1))
        #
        # Upper left diagonal
        #
        check_diagonal(p.position + Vector2d(-1, 1), Vector2d(-1, b.height), (-1, 1))
        #
        # Bottom right diagonal
        #
        check_diagonal(p.position + Vector2d(1, -1), Vector2d(b.width, -1), (1, -1))

        return self._legal_moves
