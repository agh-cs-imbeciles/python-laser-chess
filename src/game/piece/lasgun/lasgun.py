from __future__ import annotations
from typing import TYPE_CHECKING, cast

from game.observer import LaserObserver
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
        self._target_propagation_count = 2
        self._charges_left = self._charge_time
        self._board = board
        self._laser_fields: list[BoardVector2d] = []
        self._redirected: BoardVector2d | None = None
        self._last_field: BoardVector2d | None = None
        self._last_directions: BoardVector2d | None = None
        self._fired = False
        self._propagation_count = 0
        self._laser_observers = []
        self._end_hit = None



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

    @property
    def end_hit(self) -> bool:
        return self._end_hit


    def __eq__(self, other):
        return (
                super().__eq__(other)
                and self._charges_left == other.charges_left
                and self._charge_time == other.charge_time
        )

    def __str__(self):
        return "L"

    def _is_end_hit(self, origin: BoardVector2d, destination: BoardVector2d) -> bool:
        self._redirected = None

        if self._board.is_out_of_bounds(destination):
            self._end_hit = None
            return True

        piece = self._board.get_piece(destination)
        if piece is None:
            return False
        model = piece.model

        tup = ((origin - destination).x, (origin - destination).y)
        if model == PieceModel.LASGUN or model == PieceModel.PAWN:
            self._end_hit = (destination, Movement.from_tuple(tup))
            return True
        if model != PieceModel.MIRROR:
            return False
        self._redirect(origin, destination)
        if self._redirected is None:
            self._end_hit = (destination, Movement.from_tuple(tup))
            return True

        return False

    def _redirect(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
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

    def _propagate(self, curr_pos: BoardVector2d, curr_dir: BoardVector2d) -> None:
        direction = curr_dir
        next_pos = curr_pos + direction
        while not self._is_end_hit(curr_pos, next_pos):
            self._laser_fields.append(next_pos)
            if self._redirected is not None:
                direction = self._redirected
            curr_pos = next_pos
            next_pos = next_pos + direction

    def _inc_propagation_count(self) -> None:
        if self._propagation_count + 1 == self._target_propagation_count:
            self._fired = False
            self._propagation_count = 0
        self._propagation_count += 1

    def _propagate_laser_fields(self) -> list[BoardVector2d]:
        self._laser_fields.clear()
        x, y = self._direction.to_tuple()
        direction = BoardVector2d(x, y)
        self._propagate(self.position, direction)
        for obs in self._laser_observers:
            obs.on_laser_propagated(self)
        return self._laser_fields

    def add_laser_observer(self, observer: LaserObserver) -> None:
        self._laser_observers.append(observer)

    def can_fire(self) -> bool:
        return self._charges_left == 0

    def charge(self) -> None:
        self._charges_left = max(0, self.charges_left-1)

    def clear_laser_fields(self) -> None:
        self._laser_fields.clear()

    def propagate_until_target(self):
        if not self._fired:
            self._laser_fields.clear()
            # for obs in self._laser_observers:
            #     obs.on_laser_clear(self)
            return
        self._inc_propagation_count()
        self._propagate_laser_fields()

    def use_laser(self) -> None:
        if not self.can_fire():
            return
        self._propagate_laser_fields()
        self._fired = True
        self._propagation_count = 0
        self._charges_left = self._charge_time
