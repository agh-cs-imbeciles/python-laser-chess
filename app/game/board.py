from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Optional, Tuple
from utils import Vector2d
from game.observer import PositionObserver
from game.pieces import Piece
if TYPE_CHECKING:
    from game.pieces import Piece
    from game.pieces.movement import PieceMovement


class Board(PositionObserver):
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._move_number: int = 0
        self._pieces: Dict[Vector2d, Tuple[Piece, PieceMovement]] = {}

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
        # p.pop(origin, None)
        p[destination] = p.pop(origin,None)

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

    def add_piece(self, piece: Tuple[Piece, PieceMovement]) -> None:
        if not self.get_piece(piece[0].position):
            self._pieces[piece[0].position] = piece
            piece[0].add_observer(self)

    def add_pieces(self, pieces: list[Tuple[Piece, PieceMovement]]) -> None:
        for piece in pieces:
            self.add_piece(piece)

    def move_piece_if_possible(self, piece: Piece, destination: Vector2d):
        if self._move_number != piece.player_id:
            return
        piece_movement = self.get_piece_movement(piece.position)
        legal = piece_movement.get_legal_moves()
        if destination in legal:
            piece.move(destination)
            self._move_number = (self.move_number + 1) % 2




