from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import PieceModel

if TYPE_CHECKING:
    from game.observer import PositionObserver


class Piece:
    def __init__(self, model: PieceModel, position: Vector2d, player_id: int) -> None:
        self._model: PieceModel = model
        self._initial_position = position.copy()
        self._position: Vector2d = position
        self._player_id: int = player_id
        self._position_observers: [PositionObserver] = []

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return (
            self.model == other.model
            and self.initial_position == other.initial_position
            and self.position == other.position
            and self.player_id == other.player_id
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
    def position(self) -> Vector2d:
        return self._position
    
    @property
    def player_id(self) -> int:
        return self._player_id

    @player_id.setter
    def player_id(self, player_id: int) -> None:
        self._player_id = player_id

    def moved(self):
        return self.position != self._initial_position

    def add_observer(self, observer: PositionObserver) -> None:
        self._position_observers.append(observer)

    def move(self, to: Vector2d) -> None:
        origin = self._position.copy()
        self._position = to
        for observer in self._position_observers:
            observer.on_position_change(origin, to)
