from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from gui.menu import Menu
from gui.board import Board
from gui.window_manager import WindowManager

kv = Builder.load_file("wind.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
