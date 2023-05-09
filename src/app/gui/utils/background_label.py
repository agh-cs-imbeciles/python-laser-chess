from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

class BackgroundLabel(RelativeLayout):
    def __init__(self):
        super().__init__()
        l = Label()
        l.text = "lol"
        self.add_widget(l)
        with self.canvas.before:
            Color(1, 0, 0, 1)
            Rectangle(pos=self.pos, width=self.width, height=10)