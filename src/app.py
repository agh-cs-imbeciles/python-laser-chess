import asyncio
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# from kivy.uix.screenmanager import ScreenManager, Screen
import app.gui
from app.gui import Menu


class MyMainApp(App):
    def __init__(self):
        super().__init__()
        self.manager = ScreenManager()
    def build(self):
        Builder.load_file("app/templates/menu.kv")
        self.manager.add_widget(Menu(name="menu"))
        return self.manager


if __name__ == "__main__":
    MyMainApp().run()
