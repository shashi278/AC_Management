from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label

from kivymd.uix.button import MDRaisedButton

from database import Database

usernameHash = ""
passwordHash = ""

# sidenav class
class SideNav(ModalView, Database):
    pass


class AddDataLayout(ModalView, Database):
    def next_focus(self, text, ele):
        if ele == "dd" and len(text) == 2:
            self.ids.date.ids.mm.focus = True
        if ele == "mm" and len(text) == 2:
            self.ids.date.ids.yy.focus = True


# popups class
class LoginPopup(ModalView, Database):
    def login(self, username, password):
        self.username = username
        self.password = password

        if self.username == usernameHash and self.password == passwordHash:
            self.ids.warningInfo.text = ""
            self.dismiss()
            return True

        else:
            self.ids.warningInfo.text = "Wrong username or password"
            return False

    def show_password(self, field, button):
        print(button.icon)
        field.password = not field.password
        field.focus = True
        button.icon = "eye" if button.icon == "eye-off" else "eye-off"


class DeleteWarning(ModalView, Database):
    def __init__(self, id_, data, db_file, table_name, *args):
        self.id_ = id_
        self.data = data
        self.db_file = db_file
        self.table_name = table_name

        if self.id_ == "batch":
            name1 = "batch"
            val1 = str(data["fromYear"]) + "-" + str(data["toYear"])

            name2 = "course"
            val2 = data["course"]

            name3 = "stream"
            val3 = data["stream"]

            self.condition = (
                name1
                + '="'
                + val1
                + '" AND '
                + name2
                + '="'
                + val2
                + '" AND '
                + name3
                + '="'
                + val3
                + '"'
            )

        super(DeleteWarning, self).__init__(*args)
        # print(data)

    def delete(self, app, text_color):
        """
        ///delete from database code
        """
        # print(self.condition)
        conn = self.connect_database(self.db_file)
        res = self.delete_from_database(self.table_name, conn, self.condition)

        if res:
            res_text = "Successfully deleted!"
        else:
            res_text = "Error in deleting!"

        self.ids.container.clear_widgets()
        layout = GridLayout(cols=1)
        self.ids.container.add_widget(layout)
        layout.add_widget(
            Label(text=res_text, font_size=self.height / 25 + self.width / 25)
        )
        anc_layout = AnchorLayout()
        layout.add_widget(anc_layout)

        raised = MDRaisedButton()
        raised.text = "Ok"
        raised.bind(on_release=self.dismiss)
        raised.md_bg_color = app.theme_cls.accent_color
        raised.text_color = text_color
        raised.elevation_normal = 10
        anc_layout.add_widget(raised)

    def anim_in(self, instance):
        anim = Animation(pos_hint={"x": 1.4}, t="in_cubic", d=0.3)
        anim.start(instance)

    def anim_out(self, instance):
        anim = Animation(pos_hint={"x": 0.6}, t="out_cubic", d=0.3)
        anim.start(instance)
