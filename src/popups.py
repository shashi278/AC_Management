from kivy.uix.screenmanager import SwapTransition
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.snackbar import Snackbar

from sqlite3 import Error
from time import strftime

from database import Database
from animator.attention import ShakeAnimator
from create_logs import activities, create_log

usernameHash = ""
passwordHash = ""

# sidenav class
class SideNav(ModalView, Database):
    def open_personalisation(self):
        Personalisation().open()

# being used to add fee data
class AddDataLayout(ModalView, Database):
    
    def add_more_data_layout(self):
        from custom_layouts import MultipleDataLayout
        w=MultipleDataLayout()
        self.height=60*(len(self.ids.multipleDataContainer.children)+1)+230
        self.ids.multipleDataContainer.height=60*(len(self.ids.multipleDataContainer.children)+1)
        self.ids.multipleDataContainer.add_widget(w)

    def check_all_fields(self):
        count=0
        for each in self.ids.multipleDataContainer.children:
            if each.ids.paid.text==""\
             or each.ids.date.text=="Select Date"\
             or each.ids.tid.text=="":
                return False
        return True

# popups class
class LoginPopup(ModalView, Database):

    # for animation
    defaults = {
        "pos_hint": {"center_x": 0.5, "center_y": 0.5},
        "size": "",
        "opacity": 1,
        "angle": 0,
        "origin_": "",
    }

    def login(self, username, password, title, root):

        db_file = "user_main.db"
        table_name = "users" if title == "User Login" else "admin"
        validated = False

        conn = self.connect_database(db_file)
        try:
            valid_user = self.search_from_database(
                table_name, conn, "username", username, order_by="id"
            )[0]
        except (IndexError, TypeError) as e:
            validated = False
        else:
            validated = (
                True
                if username == valid_user[3] and password == valid_user[4]
                else False
            )

        if validated:
            self.ids.warningInfo.text = ""
            self.dismiss()
            root.ids.userScreen.user_name = valid_user[1]

            #userlog
            if table_name=="users":
                dnt= strftime("%d-%m-%Y %H:%M:%S")
                uname= valid_user[1]
                activity= activities["login"]
                create_log(dnt,uname,activity)


            return True
        else:
            self.ids.warningInfo.text = "Wrong username or password"
            self.reset(self.ids.util_box)
            ShakeAnimator(self.ids.util_box, duration=0.6, repeat=False).start_()
            return False

    def show_password(self, field, button):
        field.password = not field.password
        field.focus = True
        button.icon = "eye" if button.icon == "eye-off" else "eye-off"

    # for animation
    def reset(self, widget):
        for key, val in self.defaults.items():
            if key == "size":
                val = (widget.parent.width, widget.parent.height)
            setattr(widget, key, val)

    def check_caller(self, scr_name):
        if scr_name == "Admin Login":
            self.opacity = 0.6
            self.ids.scr.transition = SwapTransition()
            self.ids.scr.current = "reset"
        elif scr_name == "User Login":
            self.opacity = 0.6
            self.ids.scr.transition = SwapTransition()
            self.ids.scr.current = "reset_user"


class DeleteWarning(ModalView, Database):
    def __init__(self, id_, data, db_file, table_name, *args, **kwargs):

        self.id_ = id_
        self.data = data
        self.db_file = db_file
        self.table_name = table_name
        self.success = False  # status of deletion
        self.callback = None  # can be called after completion of any action, generally after deletion
        self.delete_detail = ""
        try:
            self.callback = kwargs["callback"]
        except:
            pass

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
            self.delete_detail = (
                "Batch: " + val1 + ", Course: " + val2 + ", Stream: " + val3
            )

        elif self.id_ == "users":
            self.condition = (
                'name = "'
                + data["name"]
                + '" AND username = "'
                + data["username"]
                + '"'
            )
            self.delete_detail = "User: {} with username {}".format(
                data["name"], data["username"]
            )

        elif self.id_ == "fee":
            self.condition = (
                'sem = "' + data["sem"] + '" AND tid = "' + data["tid"] + '"'
            )
            self.delete_detail = (
                "Sure to delete fee for sem. "
                + data["sem"]
                + "of reg. no"
                + data["reg"]
            )

        super(DeleteWarning, self).__init__(*args)

    def delete(self, app, text_color):
        """
        code for deleting from database goes here
        """
        conn = self.connect_database(self.db_file)
        res = self.delete_from_database(self.table_name, conn, self.condition)
        conn.close()

        if res:
            if self.id_ == "fee":
                if self.delete_table(self.db_file,self.table_name+"_"+self.data["sem"]):
                    self.success = True
                    res_text = "Successfully deleted!"
                    
                    if self.callback is not None:
                        self.callback()

                    ##userlog
                    dnt= strftime("%d-%m-%Y %H:%M:%S")
                    uname= self.data["uname"]
                    activity= activities["delete_fee"].format(self.data["name"],self.data["sem"])
                    create_log(dnt,uname,activity)
                else:
                    res_text = "Error in deletion!"
            else:
                self.success = True
                res_text = "Successfully deleted!"
                
                if self.callback is not None:
                    self.callback()
        else:
            res_text = "Error in deletion!"

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


class Personalisation(ModalView):
    def theme_picker_open(self):
        MDThemePicker().open()
