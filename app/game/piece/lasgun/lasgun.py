from __future__ import annotations
from typing import TYPE_CHECKING, cast

from game.observer.board_position_obs import BoardPositionObserver
from game.piece import Piece, PieceModel
from game.piece.lasgun import MirrorPiece
from game.piece.movement import Movement
from utils import BoardVector2d

if TYPE_CHECKING:
    from game import Board


class Lasgun(MirrorPiece):
    def __init__(self, position: BoardVector2d, player_id: int, direction: Movement, board: Board):
        super().__init__(position, player_id, direction)
        self._model = PieceModel.LASGUN
        self._charge_time = 5
        self._charges_left = self._charge_time
        self._board = board
        self._laser_fields: list[BoardVector2d] = []
        self._redirected: BoardVector2d | None = None
        self._last_field: BoardVector2d | None = None
        self._last_directions: BoardVector2d | None = None
        self._fired = False

    @property
    def charges_left(self) -> int:
        return self._charges_left

    @property
    def charge_time(self) -> int:
        return self._charge_time

    @property
    def laser_fields(self) -> list[BoardVector2d]:
        return self._laser_fields

    @property
    def fired(self) -> bool:
        return self._fired

    @fired.setter
    def fired(self, f: bool) -> None:
        self._fired = f

    def __eq__(self, other):
        return (
                super().__eq__(other)
                and self._charges_left == other.charges_left
                and self._charge_time == other.charge_time
        )

    def __str__(self):
        return "L"

    def move(self, destination: BoardVector2d | None = None, rotate_right: bool | None = None) -> None:
        for observer in self._position_observers:
            observer.on_position_change(self._position.copy(), destination)

    def can_fire(self):
        return self._charges_left == 0

    def clear_laser_fields(self) -> None:
        self._laser_fields.clear()

    def charge(self) -> None:
        self._charges_left = max(0, self.charges_left-1)

    def reset(self):
        self._charges_left = self._charge_time

    def __is_end_hit(self, origin: BoardVector2d, destination: BoardVector2d) -> bool:
        self._redirected = None

        if self._board.is_out_of_bounds(destination):
            return True

        piece = self._board.get_piece(destination)
        if piece is None:
            return False
        model = piece.model
        if model == PieceModel.LASGUN or model == PieceModel.PAWN:
            return True
        if model != PieceModel.MIRROR:
            return False

        self.__redirect(origin, destination)
        if self._redirected is None:
            return True

        return False

    def __redirect(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        p = self._board.get_piece(destination)
        if not isinstance(p, MirrorPiece):
            self._redirected = None
            return
        mirror = cast(MirrorPiece, p)
        dir = mirror.direction.to_tuple()
        fv = BoardVector2d(dir[0], 0)
        sv = BoardVector2d(0, dir[1])
        if mirror.position + fv == origin:
            self._redirected = BoardVector2d(0, dir[1])
        elif mirror.position + sv == origin:
            self._redirected = BoardVector2d(dir[0], 0)
        else:
            self._redirected = None


    # ready
    # aim
    def fire(self) -> list[BoardVector2d]:
        self._laser_fields.clear()
        x, y = self._direction.to_tuple()
        direction = BoardVector2d(x, y)
        self.__propagate(self.position, direction)
        # return self._laser_fields

    def continue_laser_popagation(self) -> list[BoardVector2d]:
        self.__propagate(self._last_field, self._last_directions)
        # return self._laser_fields

    def __propagate(self, curr_pos: BoardVector2d, curr_dir: BoardVector2d):
        direction = curr_dir
        next_pos = curr_pos + direction
        while not self.__is_end_hit(curr_pos, next_pos):
            self._laser_fields.append(next_pos)
            if self._redirected is not None:
                direction = self._redirected
            curr_pos = next_pos
            next_pos = next_pos + direction
        self._last_field = curr_pos
        self._last_directions = direction
