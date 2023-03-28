from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from utils import Vector2d
from game.observer import PositionObserver
from game.pieces import Piece
from game.pieces.move import PieceMoveType, PieceMoveDetector

if TYPE_CHECKING:
    from game.pieces.movement import PieceMovement


class Board(PositionObserver):
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._move_number: int = 0
        self._pieces: dict[Vector2d, tuple[Piece, PieceMovement]] = {}
        self._checked_squares: [dict[Vector2d, Piece]] = [{}, {}]

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    @property
    def move_number(self) -> int:
        return self._move_number

    @move_number.setter
    def move_number(self, value: int) -> None:
        self._move_number = value

    # override PositionObserver
    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        p = self._pieces
        # moveType = PieceMoveDetector.detect(self, self.get_piece(origin), destination)
        p[destination] = p.pop(origin, None)

    def get_size(self) -> tuple[int, int]:
        return self._width, self._height

    def get_piece(self, position: Vector2d) -> Optional[Piece]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[0]

    def get_piece_movement(self, position: Vector2d) -> Optional[PieceMovement]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[1]

    def can_move_to(self, to: Vector2d, piece: Optional[Piece] = None) -> bool:
        #
        # Check, if position after moving is in bounds of board
        #
        if to.x < 0 or to.x >= self.width or to.y < 0 or to.y >= self.height:
            return False

        #
        # Move with potential capturing
        #
        if isinstance(piece, Piece):
            p = self.get_piece(to)
            return True if not p or p.player_id != piece.player_id else False
        #
        # Move without capturing
        #
        else:
            return True if not self.get_piece(to) else False

    def is_piece_at(self, vector: Vector2d) -> bool:
        return self.get_piece(vector) is not None

    def add_piece(self, piece: tuple[Piece, PieceMovement]) -> None:
        if not self.get_piece(piece[0].position):
            self._pieces[piece[0].position] = piece
            piece[0].add_observer(self)

    def add_pieces(self, pieces: list[tuple[Piece, PieceMovement]]) -> None:
        for piece in pieces:
            self.add_piece(piece)

    def update_checked_squares(
        self, piece: Piece, origin: Vector2d, destination: Vector2d, increment: tuple[int, int]
    ) -> None:
        pass

    def check_squares(
        self, piece: Piece, origin: Vector2d, destination: Vector2d, increment: tuple[int, int]
    ) -> list[Vector2d]:
        return self.__check_squares_lmp(piece, origin, destination, increment)[0]

    def __check_squares_lmp(
        self, piece: Piece, origin: Vector2d, destination: Vector2d, increment: tuple[int, int]
    ) -> tuple[list[Vector2d], Piece | None]:
        """
        Check squares of the board and return legal moves (lm) list and optional blocking piece (p).
        :param piece: piece involved
        :param origin: origin vector of ray checking
        :param destination: destination vector of ray checking
        :param increment: x, y increment values
        :return: tuple of legal moves and optional piece, if is in the way of ray
        """

        if increment[0] == 0 and increment[1] == 0:
            raise ValueError("increment tuple must be different than (0, 0)")

        if increment[0] != 0:
            xs = [x for x in range(origin.x, destination.x, increment[0])]
        if increment[1] != 0:
            ys = [y for y in range(origin.y, destination.y, increment[1])]
        if increment[0] == 0:
            xs = [origin.x for _ in ys]
        if increment[1] == 0:
            ys = [origin.y for _ in xs]

        legal_moves = []
        blocking_piece = None
        deltas = zip(xs, ys)

        for x, y in deltas:
            pos = Vector2d(x, y)
            if not self.can_move_to(pos):
                if self.is_piece_at(pos) and piece.player_id != self.get_piece(pos).player_id:
                    legal_moves.append(pos)
                    blocking_piece = self.get_piece(pos)
                break
            legal_moves.append(pos)

        return legal_moves, blocking_piece
