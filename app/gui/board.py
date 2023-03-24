from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import Callback
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import  Screen

class Board(Screen):
    def __init__(self,**kwargs):
        super().__init__()
        grid=self.ids.board
        for i in range(8):
            for j in range(8):
                b = Button()
                b.background_normal=""
                if ((i + j) % 2 == 0):
                    b.background_color =(1,1,1,1)
                else:
                    b.background_color = (0, 0, 0, 1)
                grid.add_widget(b)

class BoardGrid(GridLayout):
    def __init__(self,**kwargs):
        super().__init__()
        for i in range(8):
            for j in range(8):
                b = Button()
                b.background_normal=""
                if ((i + j) % 2 == 0):
                    b.background_color =(1,1,1,1)
                else:
                    b.background_color = (0, 0, 0, 1)
                self.add_widget(b)
    def resize(self):
        print(self.parent.size)

