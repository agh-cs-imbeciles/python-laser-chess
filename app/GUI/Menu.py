from kivy.graphics import Rectangle
from kivy.uix.screenmanager import  Screen

class Menu(Screen):
    def __init__(self,**kwargs):
        super().__init__()
    def on_button_click(self):
        print("lol")
    def update_width(self):
        self.ids.b1.height = self.ids.b1.width/2
