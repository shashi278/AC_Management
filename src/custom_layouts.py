from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.uix.screenmanager import RiseInTransition
from kivy.utils import get_color_from_hex as C
from kivy.factory import Factory

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.snackbar import Snackbar

from database import Database
from hoverable import HoverBehavior
from custom_widgets import LabelForList, LabelForListStudent
from popups import DeleteWarning, AddDataLayout ,FeeInfoPopup

import os
from kivy.utils import platform
from os.path import sep, expanduser, isdir, dirname
from filebrowser import FileBrowser
from functools import partial


class MyTab(BoxLayout, MDTabsBase):
    orientation = "vertical"


# Being used in Manage Student section
class UpdateStudentLayout(BoxLayout):
    pass


class HoverLayout(BoxLayout, HoverBehavior):
    pass


class ListItemLayout(TouchRippleBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(ListItemLayout, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point:
            self.root = (
                self.parent.parent.parent.parent.parent.parent.parent.parent.manager
            )
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            self.root.ids.profilePage.reg_no = self.parent.ids.lbl1.text
            self.root.transition = RiseInTransition()
            self.root.current = "profilepage"
            return True
        return False


class UserInfo(BoxLayout, Database):
    def delete(self, app, root, icon):
        icon = app.root.ids.adminScreen.ids.plus.icon
        if icon != "plus":
            Snackbar(
                text="Cannot delete while in edit mode. Save ongoing edits first.",
                duration=2.5,
            ).show()
        else:
            fields = [child.children[0].text for child in root.children[-2:0:-1]]
            data = {"name": fields[0], "username": fields[2], "password": fields[3]}
            DeleteWarning(
                "users",
                data,
                "user_main.db",
                "users",
                callback=app.root.ids.adminScreen.populate_user_data,
            ).open()


# Being used in profile page
class Rowinfo(BoxLayout, Database):

    color = ListProperty()

    def edit(self, root, icon, app):
        fields = [child.children[0].text for child in root.children[1:]][-2::-1]
        sem = root.children[-1].children[0].text

        tableName = "_" + str(self.parent.reg_no)
        conn = self.connect_database("fee_main.db")

        data = self.search_from_database(tableName, conn, "sem", sem, order_by="sem")[0]
        conn.close()

        sem, late = data[0], data[3]

        tableName = "_" + str(self.parent.reg_no) + "_" + str(sem)
        data = self.extractAllData("fee_main.db", tableName, order_by="id")

        adl = AddDataLayout()
        adl.from_update = True
        adl.ids.sem.text = str(sem)
        adl.ids.sem.disabled = True

        adl.height = 60 * len(data) + 230
        adl.ids.multipleDataContainer.height = 60 * len(data)
        for c, each in enumerate(data):
            if c == 0:
                w = adl.ids.multipleDataContainer.children[0]
            else:
                if (each[5]=="Late Fine"):
                    adl.ids.lateCheckbox.active=True
                    w= adl.ids.multipleDataContainer.children[0]
                    adl.height = 60 * (len(data)) + 230
                    adl.ids.multipleDataContainer.height = 60 * (len(data))

                else:
                    w = MultipleDataLayout()
                    adl.ids.multipleDataContainer.add_widget(w)

            w.ids.paid.text = str(each[1])
            w.ids.date.text = each[2]
            w.ids.tid.text = each[3]
            w.ids.docName.text = each[4]
            w.ids.rem.text = each[5]
                
        adl.open()

    def delete(self, app, root, icon):
        fields = [child.children[0].text for child in root.children[1:]][-1::-1]
        data = {
            "sem": fields[0],
            "tid": fields[5],
            "reg": self.parent.reg_no,
            "name": self.parent.name,
            "uname": self.parent.uname,
        }
        tableName = "_" + str(self.parent.reg_no)
        DeleteWarning(
            "fee",
            data,
            "fee_main.db",
            tableName,
            callback=app.root.current_screen.populate_screen,
        ).open()

    def open_feeinfo_popup(self,root,app):
        popup=FeeInfoPopup()
        popup.reg_no=self.parent.reg_no
        popup.app=app
        popup.sem=root.sem
        popup.ids.semLabel.text="Semester[size=100][b]{}[/b][/size]".format(root.sem)
        popup.open()

class FeeInfoData(BoxLayout):
    paid=""
    date=""
    tid=""
    filename=""
    def __init__(self,paid,date,tid,filename):
        self.paid=paid
        self.date=date
        self.tid=tid
        self.filename=filename
        super().__init__()

    def view_doc(self):
        from generate_fee_receipt import show_doc
        if self.filename!="":
            extension = os.path.splitext(self.filename)[1]
            print(extension)
            if os.path.exists("documents/"+self.tid+extension):
                show_doc("documents\\"+self.tid+extension)
            else:
                Snackbar(text="Error in file showing!",duration=2).show()
            
        print(type(self.filename))

class AddUserDataLayout(FloatLayout):
    def manage_icon(self, btn):
        name = self.ids.name.text
        email = self.ids.email.text
        username = self.ids.username.text
        password = self.ids.password.text

        data = [name, email, username, password]

        if any([len(each) for each in data]):
            btn.icon = "check"
        elif not btn.icon == "plus":
            btn.icon = "window-close"


class RowFeeRecipt(BoxLayout):
    pass


class RowNotification(BoxLayout):
    def delete(self, root, app):
        fields = [child.children[0].text for child in root.children[-1:0:-1]]
        a = fields[1].split("-")
        data = {
            "sem": fields[0],
            "fromyear": a[0],
            "toyear": a[1],
            "course": fields[2],
            "stream": fields[3],
            "category": fields[4],
        }
        app.root.ids.notificationScreen.delete_data(data, app)


class RowUsersLogs(BoxLayout):
    pass


class SoftwareModeLayout(BoxLayout):

    previous_date = None

    def open_date_picker(self, app):
        self.app = app
        if self.ids.lateFine.text != "":
            from kivymd.uix.picker import MDDatePicker

            if self.previous_date is not None:
                pd = self.previous_date
                try:
                    MDDatePicker(
                        self.set_previous_date, pd.year, pd.month, pd.day
                    ).open()
                except AttributeError:
                    MDDatePicker(self.set_previous_date).open()
            else:
                MDDatePicker(self.set_previous_date).open()
        else:
            Snackbar(text="Please Fill Late Fine.", duration=2.5,).show()

    def set_previous_date(self, date_obj):

        self.previous_date = date_obj
        self.ids.dueDate.text = "/".join(str(date_obj).split("-")[::-1])
        self.app.root.ids.notificationScreen.load_message(
            self.ids.lateFine.text, self.ids.dueDate.text
        )


class MultipleDataLayout(BoxLayout):
    doc_path = ""
    previous_date = None

    def open_date_picker(self):
        from kivymd.uix.picker import MDDatePicker

        if self.previous_date is not None:
            pd = self.previous_date
            try:
                MDDatePicker(self.set_previous_date, pd.year, pd.month, pd.day).open()
            except AttributeError:
                MDDatePicker(self.set_previous_date).open()
        else:
            MDDatePicker(self.set_previous_date).open()

    def set_previous_date(self, date_obj):

        self.previous_date = date_obj
        self.ids.date.text = "-".join(str(date_obj).split("-")[::-1])

    def open_FileSelector(self, inst):

        if platform == "win":
            user_path = dirname(expanduser("~")) + sep + "Documents"
        else:
            user_path = expanduser("~") + sep + "Documents"
        self._fbrowser = FileBrowser(
            select_string="Select",
            favorites=[(user_path, "Documents")],
            filters=["*.pdf", "*.jpg", "*.jpeg", "*.png"],
        )
        self._fbrowser.bind(
            on_success=partial(self._fbrowser_success, inst),
            on_canceled=self._fbrowser_canceled,
        )

        self.fpopup = Popup(
            content=self._fbrowser,
            title_align="center",
            title="Select File",
            size_hint=(0.7, 0.9),
            auto_dismiss=False,
        )
        self.fpopup.open()

    def _fbrowser_canceled(self, instance):
        self.fpopup.dismiss()

    def _fbrowser_success(self, layoutins, instance):
        try:
            selected_path = instance.selection[0]
            if selected_path:
                layoutins.doc_path = selected_path
                layoutins.ids.docName.text = os.path.basename(selected_path)
                layoutins.ids.viewBtn.opacity = 1
                layoutins.ids.viewBtn.disabled = False
                Snackbar(text="File uploaded successfully!", duration=2).show()
            else:
                Snackbar(text="Error uploading file.", duration=2).show()
            self.fpopup.dismiss()

        except IndexError:
            Snackbar(text="Please specify a valid file path", duration=2).show()

    def show_doc(self):
        import generate_fee_receipt

        generate_fee_receipt.show_doc(self.doc_path)

    def delete(self,root):
        if len(root.parent.children)>1:
            if(root.ids.rem.text=="Late Fine"):
                root.parent.parent.parent.ids.lateCheckbox.active=False
            else:
                root.parent.height=60*(len(root.parent.children)-1)
                root.parent.parent.parent.height=60*(len(root.parent.children)-1)+230
                root.parent.remove_widget(root)
            
