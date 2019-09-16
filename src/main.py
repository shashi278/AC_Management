"""
	
	Account Management System
	Date: 24/02/2019
"""

# imports here
from kivy.app import App
from kivy.lang import Builder

"""
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    StringProperty,
    ListProperty,
)
from kivy.core.window import Window, WindowBase
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.utils import get_color_from_hex as C

from kivymd.theming import ThemeManager
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.button import (
    MDRaisedButton,
    MDRectangleFlatButton,
    MDFloatingActionButton,
)
from kivymd.uix.textfield import MDTextField, MDTextFieldRound, MDTextFieldRect
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.tab import *

import re
import xlrd
import os
from os.path import sep, expanduser, isdir, dirname
from random import choice
from time import sleep
from sqlite3 import Error
"""
from kivy.core.window import Window, WindowBase
from database import Database
from kivymd.theming import ThemeManager

# from hoverable import HoverBehavior

from screens import ScreenManager, HomeScreen, UserScreen, ProfilePage, AdminScreen

from custom_buttons import CircularToggleButton, DropBtn

# Main App
class AccountManagementSystem(App, Database):
    theme_cls = ThemeManager()
    # theme_cls.primary_palette = 'Blue'
    # theme_cls.theme_style='Light'
    # theme_cls.accent_hue= "500"

    def build(self):
        return Builder.load_file("gui.kv")


if __name__ == "__main__":

    Window.maximize()
    Window.minimum_width = 900
    Window.minimum_height = 700

    AccountManagementSystem().run()
