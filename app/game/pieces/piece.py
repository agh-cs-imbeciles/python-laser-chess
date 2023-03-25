from utils.vector2d import Vector2d
from piece_model import PieceModel

class Piece:
    def __init__(self, model, position, player_id):
        self._model = model
        self._position = position
        self._player_id = player_id

    def __str__(self):
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
            case PieceModel.MIRROR:
                return "Mirror"
        return None

    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, value):
        self._model = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
    
    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, player):
        self._player_id = player

    def move(self, to):
        self._position = to
