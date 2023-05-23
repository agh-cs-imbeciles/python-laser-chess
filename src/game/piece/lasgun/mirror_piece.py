from __future__ import annotations

from typing import TYPE_CHECKING

from game.piece import Piece

from game.piece import PieceModel
from game.piece.movement import Movement
from utils import BoardVector2d

if TYPE_CHECKING:
    from app.gui.utils import Paths

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

    def move(self, destination: BoardVector2d | None = None, rotate: Paths | None = None) -> None:
        origin = self._position.copy()
        if destination is None:
            destination = origin
        match rotate:
            case Paths.RIGHT:
                self._direction = self._direction.double_right()
            case Paths.LEFT:
                self._direction = self._direction.double_left()
            case None:
                if destination is None:
                    raise ValueError("Destination and rotation cannot have both None value")
        self._position = destination
        self._move_count += 1
        if rotate is None:
            for observer in self._position_observers:
                observer.on_position_change(origin, destination)
        else:
            for observer in self._position_observers:
                observer.on_rotation(origin, rotate)