import numpy as np
from utils.vector2d import Vector2d

class Piece:
    def __init__(self, position, playerId):
        self._position = position
        self._playerId = playerId

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def playerId(self):
        return self._playerId

    @playerId.setter
    def playerId(self, player):
        self._playerId = player

    def move(self, to):
        self._position = to
