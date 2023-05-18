import asyncio
from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
import gui
from app.client import Sender

kv = Builder.load_file("wind.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    asyncio.run(Sender.send({"greeter": "Slim Shady", "message": "Mom's spaghetti", "spaghetti": None}))
    MyMainApp().run()
