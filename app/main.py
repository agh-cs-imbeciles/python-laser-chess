

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from app.GUI.Menu import MainWindow
from app.GUI.Board import SecondWindow
from app.GUI.WindowManager import WindowManager



kv = Builder.load_file("wind.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()