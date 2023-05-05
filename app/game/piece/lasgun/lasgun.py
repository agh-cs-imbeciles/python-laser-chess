from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Board

class Lasgun:
    def __init__(self, board: Board, ):
        self._charge_time = 6
        self._charges_left = self._charge_time
