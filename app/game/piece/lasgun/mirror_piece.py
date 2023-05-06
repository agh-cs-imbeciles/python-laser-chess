from __future__ import annotations
from game.piece import Piece

from game.piece import PieceModel
from game.piece.movement import Movement
from utils import BoardVector2d


class MirrorPiece(Piece):
    def __init__(self, position: BoardVector2d, player_id: int, direction: Movement) -> None:
        super().__init__(PieceModel.MIRROR, position, player_id)
        self._direction = direction

    def __eq__(self, other):
        return super().__eq__(other) and self.direction == other.direction

    def __str__(self):
        return "M"

    @property
    def direction(self) -> Movement:
        return self._direction

    @direction.setter
    def direction(self, direction: Movement) -> None:
        self.direction = direction

    def move(self, destination: BoardVector2d | None = None, rotate_right: bool | None = None) -> None:
        origin = self._position.copy()
        if destination is None:
            destination = origin
        match rotate_right:
            case True:
                self._direction = self._direction.double_right()
            case False:
                self._direction = self._direction.double_left()
            case None:
                if destination is None:
                    raise ValueError("Destination and rotation cannot have both None value")
        self._position = destination
        self._move_count += 1
        for observer in self._position_observers:
            observer.on_position_change(origin, destination)