from typing import cast

from kivy.properties import NumericProperty
from kivy.uix.label import Label
import weakref



class CommonFontLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_size(self,instance,value):
        self.font_size = self.width/(len(self.text)/2+1)
