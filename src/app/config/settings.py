from __future__ import annotations
from enum import Enum, auto, unique


class GameSettings:
    def __init__(self, gameplay: SettingsGameplay) -> None:
        self.__gameplay: SettingsGameplay = gameplay

    @property
    def gameplay(self) -> SettingsGameplay:
        return self.__gameplay

    @gameplay.setter
    def gameplay(self, value: SettingsGameplay) -> None:
        self.__gameplay = value


@unique
class SettingsGameplay(Enum):
    LOCAL   = auto()
    ONLINE  = auto()
