class GameSettings:
    def __init__(self, online_gameplay: bool = False) -> None:
        self.__online_gameplay: bool = online_gameplay

    @property
    def online_gameplay(self) -> bool:
        return self.__online_gameplay

    @online_gameplay.setter
    def online_gameplay(self, value: bool) -> None:
        self.__online_gameplay = value
