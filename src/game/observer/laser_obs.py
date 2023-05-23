from __future__ import annotations
from abc import ABC, abstractmethod


class LaserObserver(ABC):
    def on_laser_propagated(self, lasgun) -> None:
        pass

