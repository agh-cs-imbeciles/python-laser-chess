from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

Builder.load_string("""
<JoinGamePopup@Popup>:
    name:"game_join"
    title:"Play online game"
    size_hint:0.6, 0.2
    size_hint_min:500, 260
    #size_hint_max:400, 400
    BoxLayout:
        halign:'center'
        orientation:'horizontal'
        BoxLayout:
            orientation:'vertical'
            Button:
                id:"create"
                on_press:root.create_button_clicked()
                size_hint:1,0.2
                text:'Create the new game'
            Label:
                size_hint:1,0.2
                text:'Select colour'
            GridLayout:
                size_hint:1,0.4
                cols: 2
                Label:
                    text:"Random"
                CheckBox:
                    name:"R"
                    group:'col'
                    active:True
                    allow_no_selection: False
                    on_active: root.activate(self)
                Label:
                    text:"White"
                CheckBox:
                    name:"W"
                    group:'col'
                    allow_no_selection: False
                    on_active: root.activate(self)
                Label:
                    text:"Black"
                CheckBox:
                    name:"B"
                    group:'col'
                    allow_no_selection: False
                    on_active: root.activate(self)
            Label:
                size_hint:1,0.2
                text:'Code:'+root.host_code
        AnchorLayout: 
            anchor_y:'top'    
            BoxLayout:
                size_hint:1,0.4
                orientation:'vertical'
                Button:
                    text:'Join to the existing game'
                    on_press:root.join_button_clicked()
                TextInput:
                    text:root.join_code
                    on_text:root.text_changed(self.text)
""")


class JoinGamePopup(Popup):
    activated = StringProperty("R")
    host_code = StringProperty("")
    join_code = StringProperty("0101231")
    create_clicked = BooleanProperty(False)
    join_clicked = BooleanProperty(False)

    def activate(self, value: CheckBox):
        if value.active:
            self.activated = value.name

    def text_changed(self, value: str):
        self.join_code = value

    def create_button_clicked(self):
        self.create_clicked = True

    def join_button_clicked(self):
        self.join_clicked = True



