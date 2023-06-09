from kivy.clock import Clock
from game import Game
from utils import GameEnding


class GameTimer:
    def __init__(self, game: Game, seconds_per_player: int, player_number: int = 2) -> None:
        self.__SECONDS_PER_PLAYER = seconds_per_player
        self.__game = game
        self.player_timers: list[int] = [self.__SECONDS_PER_PLAYER for i in range(player_number)]
        self.__schedule = None

    def run(self) -> None:
        # Run schedule interval, calling decrease_timer method once per second
        self.__schedule = Clock.schedule_interval(self.decrease_timer, 1)

    def decrease_timer(self, delta_time: int) -> None:
        mn = self.__game.move_number
        if self.player_timers[mn] == 0:
            self.__game.end_game((mn+1) % 2, GameEnding.TIME_END)
        self.player_timers[mn] = max(0, self.player_timers[mn]-1)
        timer1 = self.player_timers[mn]
        timer2 = self.player_timers[(mn+1) % 2]
        self.__game.set_time(mn, timer1)
        self.__game.set_time((mn+1) % 2, timer2)

    def stop(self):
        Clock.unschedule(self.__schedule)

