from kivy.properties import NumericProperty
from kivy.uix.label import Label


def change_font_size(instance, value):
    instance.font_size = value
    print(value)


class CommonFontLabel(Label):
    static_font_size = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(static_font_size=change_font_size)
        self.static_font_size = 3