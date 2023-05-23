from __future__ import annotations
from enum import Enum, unique, auto


@unique
class MessageStatus(Enum):
    SUCCESS = auto()
    ERROR   = auto()

    def __str__(self) -> str:
        match self:
            case MessageStatus.SUCCESS:
                return "success"
            case MessageStatus.ERROR:
                return "error"

    @staticmethod
    def from_str(status: str) -> MessageStatus:
        for s in MessageStatus:
            if status == str(s):
                return s

        raise ValueError("MessageStatus argument is invalid [from_str()]")


@unique
class MessageType(Enum):
    INIT = auto()
    MOVE = auto()

    def __str__(self) -> str:
        match self:
            case MessageType.INIT:
                return "init"
            case MessageType.MOVE:
                return "move"

    @staticmethod
    def from_str(type: str) -> MessageType:
        for t in MessageType:
            if type == str(t):
                return t

        raise ValueError("MessageType argument is invalid [from_str()]")