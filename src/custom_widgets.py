from kivymd.uix.list import OneLineListItem
from kivy.uix.label import Label

from hoverable import HoverBehavior


class HoverOneLineListItem(OneLineListItem, HoverBehavior):
    pass


class LabelForList(Label):
    pass
