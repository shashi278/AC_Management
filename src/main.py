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

    def on_start(self):
        Window.bind(on_close=self.close)
        Window.set_title("Account Management System: IIIT Kalyani")
        
        default_setting={
                    "theme_style": "Light",
                    "theme_primary_palette": "Blue",
                    "theme_accent_palette": "Amber"
                    }
        try:
            with open("settings.json") as jf:
                setting=json.load(jf)
            self.theme_cls.theme_style=setting["theme_style"]
            self.theme_cls.primary_palette=setting["theme_primary_palette"]
            self.theme_cls.accent_palette=setting["theme_accent_palette"]

        except IOError:
            self.theme_cls.theme_style=default_setting["theme_style"]
            self.theme_cls.primary_palette=default_setting["theme_primary_palette"]
            self.theme_cls.accent_palette=default_setting["theme_accent_palette"]
            with open('settings.json', 'w') as jf:
                json.dump(default_setting, jf,indent=4)

        except json.decoder.JSONDecodeError:
            self.theme_cls.theme_style=default_setting["theme_style"]
            self.theme_cls.primary_palette=default_setting["theme_primary_palette"]
            self.theme_cls.accent_palette=default_setting["theme_accent_palette"]
            with open('settings.json', 'r+') as jf:
                json.dump(default_setting, jf,indent=4)
        

        db_file = "user_main.db"
        conn = self.connect_database(db_file)
        try:
            self.extractAllData(db_file, "admin", order_by="id")

        except Error:
            with open("admin_record.sql") as table:
                self.create_table(table.read(), conn)
                self.insert_into_database(
                    "admin", conn, ("", "admin@example.com", "admin", "admin", "","","")
                )

    def build(self):
        return Builder.load_file("gui.kv")

    def close(self, tmp):
        with open('settings.json', 'r+') as jf:
            setting = json.load(jf)
            setting["theme_style"] = self.theme_cls.theme_style
            setting["theme_primary_palette"] = self.theme_cls.primary_palette
            setting["theme_accent_palette"] =  self.theme_cls.accent_palette
            jf.seek(0)        
            json.dump(setting, jf,indent=4)
            jf.truncate()


if __name__ == "__main__":
    Window.maximize()
    Window.minimum_width = 900
    Window.minimum_height = 600

    AccountManagementSystem().run()
