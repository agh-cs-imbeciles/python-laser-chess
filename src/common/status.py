from __future__ import annotations
from enum import Enum


class Status(Enum):
    INIT    = 0
    SUCCESS = 1
    ERROR   = 2
    MOVE    = 3

    def __str__(self) -> str:
        match self:
            case Status.INIT:
                return "init"
            case Status.SUCCESS:
                return "success"
            case Status.ERROR:
                return "error"
            case Status.MOVE:
                return "move"

    @staticmethod
    def from_str(status: str) -> Status:
        for s in Status:
            if status == str(s):
                return s

        raise ValueError("Status argument is invalid [from_str()]")
