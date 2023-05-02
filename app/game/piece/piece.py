from __future__ import annotations
from typing import TYPE_CHECKING
from utils import BoardVector2d
from game.piece import PieceModel

if TYPE_CHECKING:
    from game.observer import PositionObserver


class Piece:
    def __init__(self, model: PieceModel, position: BoardVector2d, player_id: int) -> None:
        self._model: PieceModel = model
        self._initial_position = position.copy()
        self._position: BoardVector2d = position
        self._player_id: int = player_id
        self._move_count = 0
        self._position_observers: list[PositionObserver] = []

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return (
            self.model == other.model
            and self.initial_position == other.initial_position
            and self.position == other.position
            and self.is_same_color(other)
        )

    def __ne__(self, other):
        return not self == other

    def __str__(self) -> str:
        match self._model:
            case PieceModel.KING:
                return "K"
            case PieceModel.QUEEN:
                return "Q"
            case PieceModel.PAWN:
                return ""
            case PieceModel.BISHOP:
                return "B"
            case PieceModel.ROOK:
                return "R"
            case PieceModel.KNIGHT:
                return "N"
            case PieceModel.MIRROR:
                return "M"

    @property
    def model(self) -> PieceModel:
        return self._model
        
    @property
    def initial_position(self):
        return self._initial_position

    @property
    def position(self) -> BoardVector2d:
        return self._position
    
    @property
    def player_id(self) -> int:
        return self._player_id

    @player_id.setter
    def player_id(self, player_id: int) -> None:
        self._player_id = player_id

    def moved(self):
        return self._move_count > 0

    def is_same_color(self, other: Piece | int | None) -> bool:
        if other is None:
            return False
        if isinstance(other, Piece):
            return self.player_id == other.player_id
        return self.player_id == other

    def add_observer(self, observer: PositionObserver) -> None:
        self._position_observers.append(observer)

    def move(self, destination: BoardVector2d) -> None:
        origin = self._position.copy()
        self._position = destination
        self._move_count += 1
        for observer in self._position_observers:
            observer.on_position_change(origin, destination)
