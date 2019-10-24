"""
	Account Management System
	Date: 24/02/2019
"""

# minimal main file
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window, WindowBase
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivymd.theming import ThemeManager

from database import Database
from screens import HomeScreen
from custom_buttons import CircularToggleButton

import sys
sys.excepthook= lambda *args: None

# Main App
class AccountManagementSystem(App, Database):
    theme_cls = ThemeManager()

    def on_start(self):
    	Window.bind(on_close=self.close)
    	Window.set_title("Account Management System: IIIT Kalyani")

    def build(self):
    	return Builder.load_file("gui.kv")

    def close(self,tmp):
    	print("Window Closed")


if __name__ == "__main__":
    #Window.maximize()
    #Window.minimum_width = 900
    #Window.minimum_height = 700

    AccountManagementSystem().run()
