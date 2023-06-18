from kivy.clock import Clock
from game import Game


class GameTimer:
    def __init__(self, game: Game, seconds_per_player: int, player_number: int = 2) -> None:
        self.__SECONDS_PER_PLAYER = seconds_per_player
        self.__game = game
        self.player_timers: list[int] = [self.__SECONDS_PER_PLAYER for i in range(player_number)]

    def run(self):
        # Run schedule interval, calling decrease_timer method once per second
        Clock.schedule_interval(self.decrease_timer, 1)

    def decrease_timer(self, delta_time: int) -> None:
        print("Timer")
