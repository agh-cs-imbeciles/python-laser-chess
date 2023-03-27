from utils import Vector2d
import game.pieces as pcs
import game.observer as obs


class Piece:
    def __init__(self, model: pcs.PieceModel, position: Vector2d, player_id: int) -> None:
        self._model: pcs.PieceModel = model
        self._position: Vector2d = position
        self._player_id: int = player_id
        self._position_observers: [obs.PositionObserver] = []

    def __str__(self) -> str:
        match self._model:
            case pcs.PieceModel.KING:
                return "K"
            case pcs.PieceModel.QUEEN:
                return "Q"
            case pcs.PieceModel.PAWN:
                return ""
            case pcs.PieceModel.BISHOP:
                return "B"
            case pcs.PieceModel.ROOK:
                return "R"
            case pcs.PieceModel.KNIGHT:
                return "N"
            case pcs.PieceModel.MIRROR:
                return "M"

    @property
    def model(self) -> pcs.PieceModel:
        return self._model
    
    @model.setter
    def model(self, value: pcs.PieceModel) -> None:
        self._model = value

    @property
    def position(self) -> Vector2d:
        return self._position

    @position.setter
    def position(self, position: Vector2d) -> None:
        self._position = position
    
    @property
    def player_id(self) -> int:
        return self._player_id

    @player_id.setter
    def player_id(self, player_id: int) -> None:
        self._player_id = player_id

    def add_observer(self, observer: obs.PositionObserver) -> None:
        self._position_observers.append(observer)

    def move(self, to: Vector2d) -> None:
        origin = self._position.copy()
        self._position = to
        for observer in self._position_observers:
            observer.on_position_change(origin, to)
