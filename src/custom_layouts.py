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
from popups import DeleteWarning, AddDataLayout

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
    #db table name
    tableName = "users"
    def edit(self, root, icon, app):
        fields = [child.children[0].text for child in root.children[-2:0:-1]]
        
        username= root.children[-4].children[0].text

        if icon=="pencil":
            #extract data for this user from database
            conn= self.connect_database("user_main.db")
            data= self.search_from_database(self.tableName,conn,"username",username,order_by="id")[0]
            fields= list(data[1:])

        conn = self.connect_database("user_main.db")
        c = conn.execute("select * from {}".format(self.tableName))
        fields_names = tuple([des[0] for des in c.description][1:])

        for each, text, fn in zip(root.children[::-1][1:], fields, fields_names):
            #each.clear_widgets()
            
            # if user wants to edit
            if icon == "pencil":
                self.color = [0.1, 0.1, 0.1, 1]
                self._temp = TextInputForList()
                if fn=="username":
                    self._temp.disabled=True
                
                self._temp.text = text

                each.add_widget(self._temp)
                del self._temp
            else:
                self.color = (
                    [0.7, 0.7, 0.7, 1]
                    if app.theme_cls.theme_style == "Dark"
                    else C("#17202A")
                )
                self._temp1 = LabelForList()

                if fn=="pass":
                    self._temp1.text= "********"
                else:
                    self._temp1.text = text

                #each.add_widget(self._temp1)
                self.update_database(self.tableName, conn, fn, text, "username", username)

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

        data= self.search_from_database(tableName,conn,"sem",sem,order_by="sem")[0]
        #print(data)

        adl= AddDataLayout()
        adl.from_update=True
        adl.ids.sem.text=str(data[0])
        adl.ids.sem.disabled=True
        adl.ids.paid.text=str(data[1])
        adl.ids.late.text=str(data[3])
        adl.ids.date.text=data[4]
        adl.ids.tid.text=data[5]
        adl.ids.rem.text=data[6]
        adl.open()

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