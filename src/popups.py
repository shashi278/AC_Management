from kivy.uix.screenmanager import SwapTransition
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label

from kivymd.uix.button import MDRaisedButton

from database import Database
from animator.attention import ShakeAnimator

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

    #for animation
    defaults={
        'pos_hint': {"center_x":0.5, "center_y": 0.5},
        'size': '',
        'opacity':1,
        'angle': 0,
        'origin_':''}

    def login(self, username, password, title):

        db_file= "user_main.db"
        table_name= "users" if title=="User Login" else "admin"
        validated=False

        conn= self.connect_database(db_file)
        try:
            valid_user= self.search_from_database(table_name,conn,"username",username,order_by="id")[0]
        except (IndexError,TypeError) as e:
            validated= False
        else:
            validated=True if username==valid_user[3] and password==valid_user[4] else False
        
        #Run this below code just once to create an admin with  default credentials
        '''
        with open("admin_record.sql") as table:
            self.create_table(table.read(), conn)
            self.insert_into_database('admin', conn, ('','admin@example.com','admin','admin',''))
        '''


        if validated:
            self.ids.warningInfo.text = ""
            self.dismiss()
            return True
        else:
            self.ids.warningInfo.text = "Wrong username or password"
            self.reset(self.ids.util_box)
            ShakeAnimator(self.ids.util_box, duration=.6, repeat=False).start_()
            return False

    def show_password(self, field, button):
        field.password = not field.password
        field.focus = True
        button.icon = "eye" if button.icon == "eye-off" else "eye-off"

    #for animation
    def reset(self, widget):
        for key, val in self.defaults.items():
            if key=='size':
                val=(widget.parent.width, widget.parent.height)
            setattr(widget, key, val)

    def check_caller(self,scr_name):
        if(scr_name=="Admin Login"):
            self.opacity=.3
            self.ids.scr.transition=SwapTransition()
            self.ids.scr.current='reset'
        elif(scr_name=="User Login"):
            self.opacity=.3
            self.ids.scr.transition=SwapTransition()
            self.ids.scr.current='reset_user'

class DeleteWarning(ModalView, Database):
    def __init__(self, id_, data, db_file, table_name, *args, **kwargs):
        
        self.id_ = id_
        self.data = data
        self.db_file = db_file
        self.table_name = table_name
        self.success= False     #status of deletion
        self.callback= None     #can be called after completion of any action, generally after deletion
        self.delete_detail=''
        try:
            self.callback= kwargs["callback"]
        except: pass

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
            self.delete_detail="Batch: "+val1+", Course: "+val2+", Stream: "+val3

        elif self.id_ == "users":
            self.condition=(
                'name = "'+data["name"]+'" AND username = "'+data["username"]+'" AND pass = "'+data["password"]+'"'
            )
            self.delete_detail="User: {} with username {}".format(data["name"],data["username"])
        
        elif self.id_=="fee":
            self.condition=(
                'sem = "'+data["sem"]+'" AND tid = "'+data["tid"]+'"'
            )
            self.delete_detail="Fee detail: Semester "+data["sem"]+", Trans. Id "+data["tid"]+" for reg. no. "+data["reg"]
        
        super(DeleteWarning, self).__init__(*args)


    def delete(self, app, text_color):
        """
        code for deleting from database goes here
        """
        conn = self.connect_database(self.db_file)
        res = self.delete_from_database(self.table_name, conn, self.condition)

        if res:
            self.success= True
            res_text = "Successfully deleted!"
            if self.callback is not None:
                self.callback()
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
