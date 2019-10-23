from kivymd.uix.list import OneLineListItem
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from hoverable import HoverBehavior


class HoverOneLineListItem(OneLineListItem, HoverBehavior):
    pass


class LabelForList(Label):
    pass


class LabelForListStudent(Label):
    pass

class AdminInfoLabel(BoxLayout):
    pass

class AdminInfoEditField(BoxLayout):
    pass
