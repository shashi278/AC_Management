from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.properties import (
    # ObjectProperty,
    # NumericProperty,
    # StringProperty,
    ListProperty,
)
from kivy.uix.screenmanager import RiseInTransition
from kivy.utils import get_color_from_hex as C
from kivy.factory import Factory

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.snackbar import Snackbar

from database import Database
from hoverable import HoverBehavior
from custom_textinputs import TextInputForList
from custom_widgets import LabelForList,LabelForListStudent
from popups import DeleteWarning

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
    def edit(self, root, icon, app):
        fields = [child.children[0].text for child in root.children[-2:0:-1]]
        username= root.children[-4].children[0].text

        tableName = "users"
        conn = self.connect_database("user_main.db")
        c = conn.execute("select * from {}".format(tableName))
        fields_names = tuple([des[0] for des in c.description][1:])

        for each, text, fn in zip(root.children[::-1][1:], fields, fields_names):
            each.clear_widgets()
            # if user wants to edit
            if icon == "pencil":
                self.color = [0.1, 0.1, 0.1, 1]
                self._temp = TextInputForList()
                if fn=="username":
                    self._temp.disabled=True
                self._temp.text = text
                each.add_widget(self._temp)
            else:
                self.color = (
                    [0.7, 0.7, 0.7, 1]
                    if app.theme_cls.theme_style == "Dark"
                    else C("#17202A")
                )
                self._temp1 = LabelForList()
                self._temp1.text = text
                each.add_widget(self._temp1)
                self.update_database(tableName, conn, fn, text, "username", username)

    def delete(self, app, root, icon):
        if icon != "pencil":
            Snackbar(
                text="Cannot delete while in edit mode. Save ongoing edits first.",
                duration=2.5,
            ).show()
        else:
            fields = [child.children[0].text for child in root.children[-2:0:-1]]
            data={
                "name":fields[0],
                "username": fields[2],
                "password": fields[3]
            }
            DeleteWarning("users",data,"user_main.db","users", callback=app.root.ids.adminScreen.onStartAdminScr).open()


# Being used in profile page
class Rowinfo(BoxLayout, Database):

    color = ListProperty()

    def edit(self, root, icon, app):
        fields = [child.children[0].text for child in root.children[1:]][-2::-1]
        sem = root.children[-1].children[0].text
        #print("\n\n\nsem: {}\n\n\n".format(sem))

        tableName = "_" + str(self.parent.reg_no)
        conn = self.connect_database("fee_main.db")
        c = conn.execute("select * from {}".format(tableName))
        fields_names = tuple([des[0] for des in c.description][1:])

        for each, text, fn in zip(root.children[1:][::-1][1:], fields, fields_names):
            #if not fn=="due":    #cannot edit due field
            each.clear_widgets()
            # if user wants to edit
            if icon == "pencil":
                #if fn=="due": continue    #cannot edit due field
                self.color = [0.1, 0.1, 0.1, 1]
                self._temp = TextInputForList()
                self._temp.text = text
                each.add_widget(self._temp)
            else:
                self.color = (
                    [0.7, 0.7, 0.7, 1]
                    if app.theme_cls.theme_style == "Dark"
                    else C("#17202A")
                )
                #if fn=="due": continue
                self._temp1 = LabelForList()
                self._temp1.text = text
                #print("\n\n\nEach: {}\n\n\n".format(each.text))
                each.add_widget(self._temp1)
                #if fn=="paid":  #update due field
                 #   self.update_database(tableName, conn, "due", str(self.parent.total_fee-int(text)), "sem", sem)
                self.update_database(tableName, conn, fn, text, "sem", sem)
                #app.root.current_screen.populate_screen()

    def delete(self, app, root, icon):
        if icon != "pencil":
            Snackbar(
                text="Cannot delete while in edit mode. Save ongoing edit first.",
                duration=2.5,
            ).show()
        else:
            fields = [child.children[0].text for child in root.children[1:]][-1::-1]
            data={
                "sem":fields[0],
                "tid":fields[5],
                "reg": self.parent.reg_no
            }
            tableName = "_" + str(self.parent.reg_no)
            DeleteWarning("fee",data,"fee_main.db",tableName, callback=app.root.current_screen.populate_screen).open()