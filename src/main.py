"""
	Account Management System
	Date: 24/02/2019
"""

# minimal main file

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window, WindowBase

from kivymd.theming import ThemeManager

from database import Database
from screens import ScreenManager, HomeScreen, UserScreen, ProfilePage, AdminScreen

from custom_buttons import CircularToggleButton, DropBtn

# Main App
class AccountManagementSystem(App, Database):
    theme_cls = ThemeManager()

    def build(self):
        return Builder.load_file("gui.kv")


if __name__ == "__main__":
    Window.maximize()
    Window.minimum_width = 900
    Window.minimum_height = 700

    AccountManagementSystem().run()
