import os
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from app.gui import MenuView

os.environ["KCFG_KIVY_DEFAULT_FONT"] = "['DotGothic16','app/assets/DotGothic16-Regular.ttf']"


class MyMainApp(App):
    def __init__(self):
        super().__init__()
        self.manager = ScreenManager()

        # Run the WebSocket client in the background
        # WebSocketClient().run()

    def build(self):
        Builder.load_file("app/templates/menu.kv")
        self.manager.add_widget(MenuView(name="menu"))
        # LabelBase.register(name='DotGothic16', fn_regular='app/assets/DotGothic16-Regular.ttf')
        return self.manager


if __name__ == "__main__":
    MyMainApp().run()
