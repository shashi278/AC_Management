"""
This file contains different customized widgets

Availabe classes:
-----------------
    - HoverOneLineListItem
    - LabelForList
    - LabelForListStudent
    - AdminInfoLabel
    - AdminInfoEditField
    - CustomRecycleView

"""

from kivymd.uix.list import OneLineListItem
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView

from hoverable import HoverBehavior


class HoverOneLineListItem(OneLineListItem, HoverBehavior):
    """
    This class creates hoverable list items, being used in `Admin Screen`.
    """

    pass


class LabelForList(Label):
    """
    This class creates universal label to be used in list items across this application
    """

    pass


class LabelForListStudent(Label):
    """
    Modified `Label` to be used in `generate_receipt` list section
    """

    pass


class AdminInfoLabel(BoxLayout):
    """
    Customized `Label` to show personal/credential informations of the admin
    """

    pass


class AdminInfoEditField(BoxLayout):
    """
    Custom textfields to allow editing of admin info.
    """

    pass


class CustomRecycleView(RecycleView):
    pass
