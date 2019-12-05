"""
	Account Management System
	Date: 24/02/2019
"""

# minimal main file
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window, WindowBase
from kivy.config import Config

Config.set("input", "mouse", "mouse,multitouch_on_demand")

from kivymd.theming import ThemeManager

from sqlite3 import Error

from database import Database
from screens import HomeScreen

# Main App
class AccountManagementSystem(App, Database):
    theme_cls = ThemeManager()

    def on_start(self):
        Window.bind(on_close=self.close)
        Window.set_title("Account Management System: IIIT Kalyani")
        db_file = "user_main.db"
        conn = self.connect_database(db_file)
        try:
            self.extractAllData(db_file, "admin", order_by="id")

        except Error:
            with open("admin_record.sql") as table:
                self.create_table(table.read(), conn)
                self.insert_into_database(
                    "admin", conn, ("", "admin@example.com", "admin", "admin", "")
                )

    def build(self):
        return Builder.load_file("gui.kv")

    def close(self, tmp):
        #print("Window Closed")
        pass


if __name__ == "__main__":
    Window.maximize()
    # Window.minimum_width = 900
    # Window.minimum_height = 700

    AccountManagementSystem().run()
