from utils.vector2d import Vector2d
from game.pieces.piece_model import PieceModel
from game.observer.position_obs import PositionObserver


class Piece:
    def __init__(self, model: PieceModel, position: Vector2d, player_id: int) -> None:
        self._model: PieceModel = model
        self._position: Vector2d = position
        self._player_id: int = player_id
        self._position_observers: [PositionObserver] = []

    def __str__(self) -> str:
        match self._model:
            case PieceModel.KING:
                return "King"
            case PieceModel.QUEEN:
                return "Queen"
            case PieceModel.PAWN:
                return "Pawn"
            case PieceModel.BISHOP:
                return "Bishop"
            case PieceModel.ROOK:
                return "Rook"
            case PieceModel.KNIGHT:
                return "Knight"
            case PieceModel.MIRROR:
                return "Mirror"

    @property
    def model(self) -> PieceModel:
        return self._model
    
    @model.setter
    def model(self, value: PieceModel) -> None:
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

    def move(self, to: Vector2d) -> None:
        origin = self._position.copy()
        self._position = to
        for observer in self._position_observers:
            observer.on_position_change(origin, to)
