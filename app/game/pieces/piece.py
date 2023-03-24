from abc import ABC
import numpy as np
from utils.vector2d import Vector2d

class Piece(ABC):
    def __init__(self, position):
        self.position = position
        self.delta_positions = np.empty(0)

    def move(self, to):
        self.position = to
