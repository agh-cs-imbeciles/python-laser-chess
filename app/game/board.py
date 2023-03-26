from typing import Dict, Optional
from utils.vector2d import Vector2d
from game.pieces.piece import Piece


class Board:
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._move_number: int = 0
        self._pieces: Dict[Vector2d, Piece] = {}


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

    def get_size(self) -> tuple[int, int]:
        return self._width, self._height

    def get_piece(self, position: Vector2d) -> Optional[Piece]:
        return self._pieces.get(position)

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

    def add_piece(self, piece: Piece) -> None:
        if not self.get_piece(piece.position):
            self._pieces[piece.position] = piece

    def add_pieces(self, pieces: list[Piece]) -> None:
        for piece in pieces:
            self.add_piece(piece)
