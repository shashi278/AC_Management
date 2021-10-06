"""
	Account Management System
	Date: 24/02/2019
"""

# minimal main file
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window, WindowBase
from kivy.config import Config
import json

Config.set("input", "mouse", "mouse,multitouch_on_demand")

from kivymd.theming import ThemeManager

from sqlite3 import Error

from database import Database
from screens import HomeScreen

# Main App
class AccountManagementSystem(App, Database):
    theme_cls = ThemeManager()
    default_setting = {
            "theme_style": "Light",
            "theme_primary_palette": "Blue",
            "theme_accent_palette": "Amber",
        }

    def on_start(self):
        Window.bind(on_close=self.close)
        Window.set_title("Account Management System: IIIT Kalyani")

        try:
            with open("settings.json") as jf:
                setting = json.load(jf)
            self.theme_cls.theme_style = setting["theme_style"]
            self.theme_cls.primary_palette = setting["theme_primary_palette"]
            self.theme_cls.accent_palette = setting["theme_accent_palette"]

        except IOError:
            self.theme_cls.theme_style = self.default_setting["theme_style"]
            self.theme_cls.primary_palette = self.default_setting["theme_primary_palette"]
            self.theme_cls.accent_palette = self.default_setting["theme_accent_palette"]
            with open("settings.json", "w") as jf:
                json.dump(self.default_setting, jf, indent=4)

        except json.decoder.JSONDecodeError:
            self.theme_cls.theme_style = self.default_setting["theme_style"]
            self.theme_cls.primary_palette = self.default_setting["theme_primary_palette"]
            self.theme_cls.accent_palette = self.default_setting["theme_accent_palette"]
            with open("settings.json", "r+") as jf:
                json.dump(self.default_setting, jf, indent=4)

        db_file = "user_main.db"
        try:
            self.extractAllData(db_file, "admin", order_by="id")

        except Error:
            with open("admin_record.sql") as table:
                conn = self.connect_database(db_file)
                self.create_table(table.read(), conn)
                #conn = self.connect_database(db_file)
                self.insert_into_database(
                    "admin",
                    conn,
                    ("Admin", "admin@example.com", "admin", "admin", "", "", ""),
                )
                conn.close()

    def build(self):
        return Builder.load_file("gui.kv")

    def close(self, tmp):
        with open("settings.json", "r+") as jf:
            setting = json.load(jf)
            setting["theme_style"] = self.theme_cls.theme_style
            setting["theme_primary_palette"] = self.theme_cls.primary_palette
            setting["theme_accent_palette"] = self.theme_cls.accent_palette
            jf.seek(0)
            json.dump(setting, jf, indent=4)
            jf.truncate()


if __name__ == "__main__":
    # Does not seem to work on Linux with SDL2 provider :(
    Window.maximize()
    Window.minimum_width = 900
    Window.minimum_height = 600

    AccountManagementSystem().run()
