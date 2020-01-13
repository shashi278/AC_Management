from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    RiseInTransition,
    SwapTransition,
)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import (
    MDRaisedButton,
    MDRectangleFlatButton,
    MDFloatingActionButton,
    MDIconButton,
)
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.list import (
    ILeftBody,
    ILeftBodyTouch,
    IRightBodyTouch,
    OneLineIconListItem,
    OneLineListItem,
)

# internal imports
import os
import threading
from os.path import sep, expanduser, isdir, dirname
from random import choice
from sqlite3 import Error
from functools import partial
import asyncio
import random
import smtplib
from email.message import EmailMessage
import socket
from time import strftime
import shutil

# local imports
from database import Database
from popups import LoginPopup, DeleteWarning, SideNav, AddDataLayout
from custom_layouts import UpdateStudentLayout
from custom_widgets import AdminInfoLabel, AdminInfoEditField
from custom_buttons import DropBtn
from dropdowns import *
from generate_fee_receipt import generate_pdf, generate_batch_fee_pdf
from custom_widgets import CustomRecycleView
from create_logs import activities, create_log, extract_log

# left iconbutton
class ListLeftIconButton(ILeftBodyTouch, MDIconButton):
    pass


# right iconbutton,checkbox,switch
class ListRightIconButton(IRightBodyTouch, MDIconButton):
    pass


class ListRightCheckBox(IRightBodyTouch, MDCheckbox):
    pass


class ListRightSwitch(IRightBodyTouch, MDSwitch):
    pass


# ScreenManager Class
class ScreenManager(ScreenManager):
    pass


# HomeScreen Class
class HomeScreen(Screen):
    def openLoginPop(self, title):
        """Opens up the login popup with desired title

        :param title: Title for the popup (Currently can be either of Admin or User)
        :type title: str
        """
        lp = LoginPopup()
        lp.ids.loginTitle.text = "{} Login".format(title)
        lp.ids.username_.focus = True
        lp.open()


# UserScreen
class UserScreen(Screen, Database):
    """
    User Screen class
    """

    def onStartUserScr(self):
        """
        Function to get called everytime user screen starts
        """
        # --------------Update Student list---------------------#
        self.ids.rv.data = []
        try:
            data_list = self.extractAllData("student_main.db", "General_record")
            for counter, each in enumerate(data_list, 1):
                x = {
                    "sno": counter,
                    "reg": each[0],
                    "name": each[1],
                    "course": each[2],
                    "stream": each[3],
                    "batch": each[4],
                }
                self.ids.rv.data.append(x)
        # if no data then pass
        except:
            pass

    def onSelect(self, btn, mainBtn):
        """

        """
        mainBtn.text = btn.text

    def anim_in(self, instance):
        """
        Animation to open sidenav

        :param instance: Object instance to be animated
        :type instance: `popups.SideNav`
        """
        anim = Animation(pos_hint={"x": -0.3}, t="in_cubic", d=0.3)
        anim.start(instance)

    def anim_out(self, instance):
        """
        Animation to close sidenav

        :param instance: Object instance to be animated
        :type instance: `popups.SideNav`
        """
        anim = Animation(pos_hint={"x": 0}, t="out_cubic", d=0.3)
        anim.start(instance)

    def open_sideNav(self):
        """
        Actual function to open-up the sidenav popup
        """
        sn = SideNav()
        sn.ids.user_name.text = self.user_name
        sn.open()

    def search(self, text):
        """
		Dynamic search function to search database against a given text and populate
        the view in real-time

        :param text: text to be searched for
        :type text: str
        
		"""
        if not text:
            self.onStartUserScr()
            return

        filtered_list = []
        conn = self.connect_database("student_main.db")

        try:
            text = int(text)
            prop_list = ["reg"] if len(str(text)) < 4 else ["reg", "batch"]

        except:
            prop_list = ["stream", "course", "name", "batch"]

        for prop in prop_list:
            filtered_list.extend(
                self.search_from_database("General_record", conn, prop, text)
            )

        self.populate_on_search(sorted(list(set(filtered_list))))

    def populate_on_search(self, filtered_list):
        """
        Function to be called after dynamically searching from database to update
        the view in real-time

        :param filtered_list: A filtered list from which data to be fetched and updated in the view
        """
        self.ids.rv.data = []

        for counter, each in enumerate(filtered_list, 1):
            x = {
                "sno": counter,
                "reg": each[0],
                "name": each[1],
                "course": each[2],
                "stream": each[3],
                "batch": each[4],
            }
            self.ids.rv.data.append(x)


# ProfilePage
class ProfilePage(Screen, Database):

    reg_no = 0
    color = StringProperty("")
    colors = [
        "#C0392B",
        "#E74C3C",
        "#9B59B6",
        "#8E44AD",
        "#2980B9",
        "#3498DB",
        "#1ABC9C",
        "#16A085",
        "#27AE60",
        "#2ECC71",
        "#D4AC0D",
        "#F39C12",
        "#E67E22",
        "#D35400",
    ]

    def on_enter(self, *args):
        """
        Overiding `on_enter` method from `Screen`
        This function is called everytime profile page screen starts

        Currently it updates each student's info and populated the screen with corres. fee data
        """
        self.color = choice(self.colors)
        self.populate_screen()
        self.extract_data("student_main.db", "General_record")
        self.ids.rb.reg_no = self.reg_no

        Clock.schedule_interval(self.set_button_width, 0)
        Clock.schedule_interval(self.set_name_info, 0)
        Clock.schedule_interval(self.set_roll_info, 0)
        Clock.schedule_interval(self.set_email_info, 0)
        Clock.schedule_once(self.schedule, 0.5)

        Animation(opacity=1, d=0.5).start(self.ids.box)

    def schedule(self, interval):
        """
        Animating all data at once causes latency thus this function is used to update 
        another set of data after animating one set of data hile entering

        :param interval: It is sent by `Clock.schedule_once` which has no use in here
        """
        Clock.schedule_interval(self.set_course_info, 0.01)
        Clock.schedule_interval(self.set_stream_info, 0.01)
        Clock.schedule_interval(self.set_batch_info, 0.01)
        Clock.schedule_interval(self.set_fee_info, 0.01)

    def on_leave(self, *args):
        """
        Overriding `on_leave` from `Screen`

        Currently it clears up already filled data from all the fields 
        """
        self.ids.name.text = ""
        self.ids.roll.text = ""
        self.ids.email.text = ""
        self.ids.course.info_name = ""
        self.ids.stream.info_name = ""
        self.ids.batch.info_name = ""
        self.ids.fee.info_name = ""
        self.ids.rv.data = []

    def set_name_info(self, interval):
        """
        Function to produce animation effect during setting name

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        try:
            self.ids.name.text += next(self.n)
        except StopIteration:
            Clock.unschedule(self.set_name_info)

    def set_roll_info(self, interval):
        """
        Function to produce animation effect during setting roll or reg. no.

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        try:
            self.ids.roll.text += next(self.r)
        except StopIteration:
            Clock.unschedule(self.set_roll_info)

    def set_email_info(self, interval):
        """
        Function to produce animation effect during setting email

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        try:
            self.ids.email.text += next(self.e)
        except StopIteration:
            Clock.unschedule(self.set_email_info)

    def set_course_info(self, interval):
        """
        Function to produce animation effect during setting course

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        try:
            self.ids.course.info_name += next(self.c)
        except StopIteration:
            Clock.unschedule(self.set_course_info)

    def set_stream_info(self, interval):
        """
        Function to produce animation effect during setting stream

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        try:
            self.ids.stream.info_name += next(self.s)
        except StopIteration:
            Clock.unschedule(self.set_stream_info)

    def set_batch_info(self, interval):
        """
        Function to produce animation effect during setting batch

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        try:
            self.ids.batch.info_name += next(self.b)
        except StopIteration:
            Clock.unschedule(self.set_batch_info)

    def set_fee_info(self, interval):
        """
        Function to produce animation effect during setting total fee

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        try:
            self.ids.fee.info_name += next(self.f)
        except StopIteration:
            Clock.unschedule(self.set_fee_info)

    def set_button_width(self, interval):
        """
        Function to produce animation effect during setting width of the button

        :param interval: It is sent by `Clock.schedule_interval` which has no use in here
        """
        self.ids.button.width = Window.width - (dp(50) + self.ids.button.height)

    def extract_data(self, db_name, table_name):
        """
        Function to extract all data from a given table in a database.
        It not only extract the data but also sets them so that they
        could be used for producing animation effect

        :param db_name: Name of the .db file
        :type db_name: str
        :param table_name: Name of the table
        :type table_name: str

        """
        conn = self.connect_database(db_name)

        try:
            self.data_tuple = self.search_from_database(
                table_name, conn, "reg", self.reg_no
            )[0]
            self.r = iter(list("Registration Number: {}".format(self.data_tuple[0])))
            self.n = iter(list(self.data_tuple[1]))
            self.e = iter(list("Email ID: {}".format(self.data_tuple[6])))
            self.b = iter(list(self.data_tuple[4]))
            self.c = iter(list(self.data_tuple[2]))
            self.s = iter(list(self.data_tuple[3]))
            self.f = iter(list(str(self.data_tuple[5])))
            self.total_fee = self.data_tuple[5]
            self.ids.rb.total_fee = self.total_fee
            self.ids.rb.name = self.data_tuple[1]
            self.ids.rb.uname = self.parent.ids.userScreen.user_name

        except Exception as e:
            Snackbar(text="Error retrieving data: {}".format(e), duration=2).show()

    def open_add_data_layout(self):
        """
        Simple function just to open up the add fee data layout
        """
        AddDataLayout().open()

    def add_fee_data(self, ins):
        """
        Add new fee data for a student.

        It actually validates the fee data inserted and if
        it seems good then inserts them to the database storing fee data.

        :param ins: Object instance to extract data fields from. In this 
                    case it should be the instance of the popup
        :type ins: `popups.AddDataLayout`
        """
        table_name = "_" + str(self.reg_no)
        conn = self.connect_database("fee_main.db")

        sem = (
            None
            if not ins.ids.sem.text or int(ins.ids.sem.text) == 0
            else ins.ids.sem.text
        )

        if not sem:
            Snackbar(text="Semester is either empty or 0", duration=0.8).show()
            return

        if ins.check_all_fields():
            conn = self.connect_database("fee_main.db")
            table_name = "_" + str(self.reg_no) + "_" + str(sem)

            # create table
            if conn is not None:
                with open("sem_record.sql") as table:
                    self.create_table(table.read().format(table_name), conn)

            data_list = ins.ids.multipleDataContainer.children[::-1]

            tot_paid = 0
            late=0

            dataset = []
            for cont in data_list:
                paid = cont.ids.paid.text
                if(cont.ids.rem.text=="Late Fine"):
                    late=int(cont.ids.paid.text)
                    tot_paid += 0
                else:
                    tot_paid += int(paid)

                date = cont.ids.date.text
                tid = cont.ids.tid.text
                rem = cont.ids.rem.text
                doc_file = (
                    ""
                    if cont.ids.docName.text == "Upload File"
                    else cont.ids.docName.text
                )

                data = (paid, date, tid, doc_file, rem)
                dataset.append(data)

            due = self.total_fee - tot_paid
            last_date = data_list[-1].ids.date.text
            last_tid = data_list[-1].ids.tid.text
            last_rem = data_list[-1].ids.rem.text
            last_doc_file = (
                ""
                if data_list[-1].ids.docName.text == "Upload File"
                else data_list[-1].ids.docName.text
            )

            data = (sem, tot_paid, due, late, last_date, last_tid, last_rem)

            table_name = "_" + str(self.reg_no)
            #conn = self.connect_database("fee_main.db")
            if self.insert_into_database(table_name, conn, data) is not None:
                self.populate_screen()
                ins.dismiss()

                table_name = "_" + str(self.reg_no) + "_" + str(sem)
                for each in dataset:
                    self.insert_into_database(table_name, conn, each)

                self.move_doc(ins)
                ##userlog
                dnt = strftime("%d-%m-%Y %H:%M:%S")
                uname = self.parent.ids.userScreen.user_name
                activity = activities["add_fee"].format(self.data_tuple[1], sem)
                create_log(dnt, uname, activity)
            else:
                Snackbar(
                    text="Data for semester {} already exists.".format(sem), duration=1
                ).show()
            conn.close()

        else:
            Snackbar(text="Please fill up all required fields").show()

    def move_doc(self, ins):
        """
        This function saves a copy of
        documents in the source folder 
        """
        if not os.path.exists("documents/"):
            os.makedirs("documents/")

        for each in ins.ids.multipleDataContainer.children:
            if each.doc_path != "":
                extension = os.path.splitext(each.doc_path)[1]
                shutil.copy(each.doc_path, "documents/" + each.ids.tid.text + extension)

    def update_fee_data(self, ins):
        """
        Update an existing fee data for a student.

        It actually validates the fee data inserted and if
        it seems good then updates them in the database storing the fee data.

        :param ins: Object instance to extract data fields from. In this
                    case it should be the instance of the popup
        :type ins: `popups.AddDataLayout`
        """
        sem = (
            None
            if not ins.ids.sem.text or int(ins.ids.sem.text) == 0
            else ins.ids.sem.text
        )

        if not sem:
            Snackbar(text="Semester is either empty or 0", duration=0.8).show()
            return

        if ins.check_all_fields():

            data_list = ins.ids.multipleDataContainer.children[::-1]

            tot_paid = 0
            late=0

            dataset = []
            for cont in data_list:
                paid = cont.ids.paid.text
                if(cont.ids.rem.text=="Late Fine"):
                    late=int(cont.ids.paid.text)
                    tot_paid += 0
                else:
                    tot_paid += int(paid)

                date = cont.ids.date.text
                tid = cont.ids.tid.text
                rem = cont.ids.rem.text
                doc_file = (
                    ""
                    if cont.ids.docName.text == "Upload File"
                    else cont.ids.docName.text
                )

                data = (paid, date, tid, doc_file, rem)
                dataset.append(data)

            due = self.total_fee - tot_paid
            last_date = data_list[-1].ids.date.text
            last_tid = data_list[-1].ids.tid.text
            last_rem = data_list[-1].ids.rem.text
            last_doc_file = (
                ""
                if data_list[-1].ids.docName.text == "Upload File"
                else data_list[-1].ids.docName.text
            )

            data = (tot_paid, due, late, last_date, last_tid, last_rem)

            table_name = "_" + str(self.reg_no)
            conn = self.connect_database("fee_main.db")
            c = conn.execute("select * from {}".format(table_name))
            fields_names = tuple([des[0] for des in c.description][1:])
            
            if self.update_database(table_name, conn, fields_names, data, "sem", sem) is not None:
                conn.close()

                table_name = "_" + str(self.reg_no) + "_" + str(sem)
                self.delete_all_data("fee_main.db", table_name)
                conn = self.connect_database("fee_main.db")
                all_okay = True
                for each in dataset:
                    if self.insert_into_database(table_name, conn, each) is None:
                        Snackbar(text="Duplicate transaction ID", duration=1).show()
                        all_okay = False
                        break

                if all_okay:
                    self.populate_screen()
                    ins.dismiss()
                    conn.close()
                    self.move_doc(ins)
                    ##userlog
                    dnt = strftime("%d-%m-%Y %H:%M:%S")
                    uname = self.parent.ids.userScreen.user_name
                    activity = activities["edit_fee"].format(self.data_tuple[1], sem)
                    create_log(dnt, uname, activity)
            else:
                Snackbar(text="Duplicate transaction ID", duration=1).show()
        else:
            Snackbar(text="Please fill up all required fields").show()

    def populate_screen(self):
        """
        Visual presentation of the modified/added fee data list

        Extracts the required fee data from the database and updates the view
        """
        self.ids.rv.data = []
        # try to populate the screen with data already available in the corresponding
        # reg. no. table
        try:
            data_list = self.extractAllData(
                "fee_main.db", "_" + str(self.reg_no), order_by="sem"
            )
            for data_tuple in sorted(data_list):
                _temp = {
                    "sem": str(data_tuple[0]),
                    "paid": str(data_tuple[1]),
                    "due": str(data_tuple[2]),
                    "late": str(data_tuple[3]),
                    "date": str(data_tuple[4]),
                    "tid": data_tuple[5],
                    "remarks": data_tuple[6],
                }
                self.ids.rv.data.append(_temp)
        except:
            # else create table
            conn = self.connect_database("fee_main.db")
            if conn is not None:
                with open("fee_record.sql") as table:
                    self.create_table(table.read().format("_" + str(self.reg_no)), conn)
            conn.close()

    def anim_in(self, instance):
        """
        Animation to open AddDataLayout

        :param instance: Object instance to be animated
        :type instance: `popups.AddDataLayout`
        """
        anim = Animation(pos_hint={"y": -0.3}, t="in_cubic", d=0.3)
        anim.start(instance)

    def anim_out(self, instance):
        """
        Animation to close AddDataLayout

        :param instance: Object instance to be animated
        :type instance: `popups.AddDataLayout`
        """
        anim = Animation(pos_hint={"y": 0}, t="out_cubic", d=0.3)
        anim.start(instance)

    def print_pdf(self):
        """
        Generate pdf of the current view(Fee data)

        Extract all related data for the current student and use 
        `generate_pdf` to generate pdf with the current details
        """
        student_info = {
            "name": self.data_tuple[1],
            "reg": str(self.data_tuple[0]),
            "batch": self.data_tuple[4],
            "course": self.data_tuple[2],
            "stream": self.data_tuple[3],
            "fee": str(self.data_tuple[5]),
        }

        try:
            data_list = self.extractAllData(
                "fee_main.db", "_" + str(self.reg_no), order_by="sem"
            )
            sem_fee_data=[]
            for each in data_list:
                tableName = "_" + str(self.reg_no) + "_" + str(each[0])
                data = self.extractAllData("fee_main.db", tableName, order_by="id")
                instalment_fee_data=[]
                for each1 in data:
                    instalment_fee_data.append({
                        "ppaid":str(each1[1]),
                        "date":each1[2],
                        "tid":each1[3],
                    })
                sem_fee_data.append({
                    "sem":str(each[0]),
                    "paid":str(each[1]),
                    "due":str(each[2]),
                    "late":str(each[3]),
                    "fee":instalment_fee_data,
                })

                
        except Error:
            Snackbar(
                text="Error retrieving fee data for reg_no {}".format(self.reg_no),
                duration=2,
            ).show()
        else:
            if len(data_list):
                generate_pdf(student_info, sem_fee_data, None)
                Snackbar(
                    text="PDF generated for reg. no. {}".format(self.reg_no), duration=2
                ).show()
                # userlog
                dnt = strftime("%d-%m-%Y %H:%M:%S")
                uname = self.parent.ids.userScreen.user_name
                activity = activities["print_fee"].format(self.reg_no)
                create_log(dnt, uname, activity)
            else:
                Snackbar(
                    text="No fee data found for reg. no. {}".format(self.reg_no),
                    duration=2,
                ).show()


# AdminScreen
class AdminScreen(Screen, Database):
    """
    Admin screen class
    """

    pc_username = os.getlogin()

    admin_password = ""
    not_mail = ""
    not_mail_password = ""

    def onStartAdminScr(self):
        """
        Function to get call everytime admin screen starts

        It populates all admin related stuffs and performs
        some other tasks upon opening admin screen
        """

        Clock.schedule_once(self.populate_admin_info, 0)
        Clock.schedule_once(self.populate_admin_username, 0)
        Clock.schedule_once(self.populate_admin_password, 0)
        Clock.schedule_once(self.populate_not_mail, 0)
        Clock.schedule_once(self.populate_not_mail_password, 0)

        self.ids.logoutbtn.ids.lbl_txt.text_size = (sp(80), sp(80))
        self.ids.logoutbtn.ids.lbl_txt.font_size = sp(40)
        self.populate_user_data()
        # self.populate_userslog()
        # --------------------------------------------#

    def change_screen(self, instance):
        """
        Checks each screen if none is busy then changes the screen
        otherwise shows a message showing cannot go back while editing
        or something similar

        :param instance: Instance of the screen to change from
        """
        if instance.text == "Manage User" and self.check_edits_admin():
            self.ids.top_bar.text = "Admin: " + instance.text
            self.ids.scrManager.current = "manageUser"

        elif (
            instance.text == "Manage Student"
            and self.check_edits_admin()
            and self.check_edits_users()
        ):
            self.ids.top_bar.text = "Admin: " + instance.text
            self.ids.scrManager.current = "manageStudent"

        elif instance.text == "Admin Setting" and self.check_edits_users():
            self.ids.top_bar.text = "Admin: " + instance.text
            self.ids.scrManager.current = "adminSetting"

        elif (
            instance.text == "Users Logs"
            and self.check_edits_users()
            and self.check_edits_admin()
        ):
            self.ids.top_bar.text = "Admin: " + instance.text
            self.populate_userslog()
            self.ids.scrManager.current = "usersLogs"

    def check_edits_admin(self):
        """
        Check if nothing is in edit mode in the admin info screen

        :returns: True: if nothing is in edit mode and its good to change the screen
        :returns False: Otherwise
        """
        if (
            self.ids.adminInfoEditBtn.icon == "check"
            or self.ids.adminPasswordEditBtn.icon == "check"
            or self.ids.adminUsernameEditBtn.icon == "check"
            or self.ids.notMailEditBtn.icon == "check"
            or self.ids.notMailPassEditBtn.icon == "check"
        ):
            Snackbar(text="Kindly save ongoing edits.", duration=2,).show()
            return False
        else:
            return True

    def check_edits_users(self):
        """
        Check if nothing is in edit mode in the manage user screen

        :returns: True: if nothing is in edit mode and its good to change the screen
        :returns False: Otherwise
        """
        if not self.ids.plus.icon == "plus":
            Snackbar(text="Kindly save ongoing edits.", duration=2,).show()
            return False
        return True

    def add_user_layout(self, layout, btn):
        """
        Adds layout to add/modify users

        It really does some hacky stuffs to ensure smooth working of layout
        either for adding a new user or modifying an existing one.

        :param layout: FloatLayout instance which is the actual layout where data is inserted
        :param btn: Button to close/open the layout

        """
        if btn.icon == "plus":
            # clear any previous data it might have
            layout.children[3].text = ""
            layout.children[2].text = ""
            layout.children[1].text = ""
            layout.children[1].disabled = False
            layout.children[0].text = ""
            self._user_layout_anim_out(layout)
            btn.icon = "window-close"

        elif btn.icon == "check":
            # extract data
            name = layout.children[3].text.strip()
            email = layout.children[2].text.strip()
            username = layout.children[1].text.strip()
            password = layout.children[0].text.strip()

            data = (name, email, username, password)

            if not all([len(each) for each in data]):
                Snackbar(text="Fields cannot be empty", duration=0.3).show()
            else:
                conn = self.connect_database("user_main.db")
                if layout.parent.from_update:
                    layout.parent.from_update = False
                    c = conn.execute("select * from {}".format("users"))
                    fields = tuple([des[0] for des in c.description][1:])
                    if not self.update_database(
                        "users", conn, fields, data, "username", username
                    ):
                        Snackbar(text="Error updating database", duration=0.3).show()
                    else:
                        Snackbar(
                            text="Database updated for {}".format(username),
                            duration=0.6,
                        ).show()
                        self.populate_user_data()
                        self._user_layout_anim_in(layout)
                        btn.icon = "plus"

                else:
                    try:
                        if not self.insert_into_database("users", conn, data):
                            raise Error
                        else:
                            self.populate_user_data()
                            self._user_layout_anim_in(layout)
                            btn.icon = "plus"
                    except Error:
                        # if table doesn't exist
                        with open("user_record.sql", "r") as table:
                            self.create_table(table.read().format("users"), conn)
                            if not self.insert_into_database("users", conn, data):
                                Snackbar(
                                    text="Username already exists", duration=0.3
                                ).show()
                            else:
                                self.populate_user_data()
                                self._user_layout_anim_in(layout)
                                btn.icon = "plus"
                conn.close()

        else:
            self._user_layout_anim_in(layout)
            btn.icon = "plus"

    def _user_layout_anim_out(self, widget):
        """
        Animated opening of layout for adding user
        """
        anim = Animation(d=0.4, y=0)
        anim.start(widget)

    def _user_layout_anim_in(self, widget):
        """
        Animated closing of layout for adding user
        """
        anim = Animation(d=0.4, y=-widget.height)
        anim.start(widget)

    def populate_user_data(self):
        """
        Function to populate/refresh the user list in the manage user section
        """
        # --------------Update User info Data List ---------------------#
        self.ids.rv.data = []

        try:
            # data may not be present
            data_list_users = self.extractAllData(
                "user_main.db", "users", order_by="id"
            )
            for counter, each in enumerate(data_list_users, 1):
                x = {
                    "sno": str(counter),
                    "name": each[1],
                    "email": each[2],
                    "username": each[3],
                    "password": "********",
                }
                self.ids.rv.data.append(x)
        except (TypeError, Error):
            pass

    def update_user_info(self, layout, btn, inst):
        """
        Function to update user info

        :param layout: The layout containing the actual data
        :param btn: The button to open/close the layout
        :param inst: Object instance to extract user information from
        """
        texts = [child.children[0].text for child in inst.children[-2:0:-1]]
        username = texts[2]

        conn = self.connect_database("user_main.db")
        data = self.search_from_database(
            "users", conn, "username", username, order_by="id"
        )[0]
        data = list(data[1:])

        layout.children[3].text = data[0]
        layout.children[2].text = data[1]
        layout.children[1].text = data[2]
        layout.children[1].disabled = True
        layout.children[0].text = data[3]
        self._user_layout_anim_out(layout)
        btn.icon = "check"

    def connectFileSelector(self, fromYear, toYear, course, stream, fee):
        """
        Function to validate input data before opening the actual file stream for selection a file

        :param fromYear: from-year
        :param toYear: to-year
        :param course: course
        :param stream: stream
        :param fee: fee
        """
        if fromYear == "" or toYear == "" or fee == "":
            Snackbar(text="Please fill in all required fields.", duration=2).show()

        elif course == "Select Course":
            Snackbar(text="Please select a course.", duration=2).show()

        elif stream == "Select Stream":
            Snackbar(text="Please select a stream.", duration=2).show()

        else:
            self.fields = {
                "fromYear": fromYear,
                "toYear": toYear,
                "course": course,
                "stream": stream,
                "fee": fee,
            }
            self.open_FileSelector()

    def open_FileSelector(self):
        """
        open filebrowser popup
        """

        if platform == "win":
            user_path = dirname(expanduser("~")) + sep + "Documents"
        else:
            user_path = expanduser("~") + sep + "Documents"
        self._fbrowser = FileBrowser(
            select_string="Select",
            favorites=[(user_path, "Documents")],
            filters=["*.xls", "*.xlsx"],
        )
        self._fbrowser.bind(
            on_success=self._fbrowser_success, on_canceled=self._fbrowser_canceled
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
        """
        Called when cancel button is pressed on the popup
        """
        self.fpopup.dismiss()

    def _fbrowser_success(self, instance):
        """
        Called when select button is pressed on the popup

        It uploads the provided .xlsx file to the database
        and shows success or error message accordingly
        """
        try:
            selected_path = instance.selection[0]
            #set cursor to wait
            Window.set_system_cursor("wait")

            with open("general_record.sql") as table:
                if self.readFile(
                    "student_main.db",
                    table.read(),
                    "General_record",
                    selected_path,
                    fromYear=self.fields["fromYear"],
                    toYear=self.fields["toYear"],
                    course=self.fields["course"],
                    stream=self.fields["stream"],
                    fee=self.fields["fee"],
                ):
                    Snackbar(text="File uploaded successfully!", duration=2).show()
                else:
                    Snackbar(text="Error uploading file.", duration=2).show()
            self.fpopup.dismiss()
            #set cursor back to arrow
            Window.set_system_cursor("arrow")

        except IndexError:
            Snackbar(text="Please specify a valid file path", duration=2).show()

    # -----------------------select Course and Stream---------------------------------------------#
    def openCourseList(self, instance):
        """
        Function to open course dropdown
        """
        dropdown = CourseDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def openStreamList(self, instance):
        """
        Function to open stream dropdown
        """
        dropdown = StreamDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def onSelect(self, btn, mainBtn):
        """
        This function is called whenever a button is selected from the dropdown

        :param btn: instance of selected dropdown button
        :param mainBtn: instance of main button of the dropdown
        """
        mainBtn.text = btn.text

    def deleteBatch(self, fromYear, toYear, course, stream):
        """
        Delets a selected batch from database

        :param fromYear: from-year of the batch
        :param toYear: to-year of the batch
        :param course: course
        :param stream: stream
        """

        if fromYear == "" or toYear == "":
            Snackbar(text="Please fill in all required fields.", duration=2).show()

        elif course == "Select Course":
            Snackbar(text="Please select a course.", duration=2).show()

        elif stream == "Select Stream":
            Snackbar(text="Please select a stream.", duration=2).show()

        else:
            data = {
                "fromYear": fromYear,
                "toYear": toYear,
                "course": course,
                "stream": stream,
            }
            DeleteWarning("batch", data, "student_main.db", "General_record").open()

    def checkBeforeUpdate(self, reg_no, parent):
        """
        Validates the provided registration number before updating a student info

        :param reg_no: registration number to be updated
        :param parent: Layout in which fetched details will be added
        """
        if len(reg_no) == 3 and len(parent.children) == 0:
            try:
                conn = self.connect_database("student_main.db")
                data_tuple = self.search_from_database(
                    "General_record", conn, "reg", reg_no
                )[0]
                if len(data_tuple) != 0:
                    update_layout = UpdateStudentLayout()
                    update_layout.name = data_tuple[1]
                    update_layout.course = data_tuple[2]
                    update_layout.stream = data_tuple[3]
                    update_layout.batch = data_tuple[4]
                    update_layout.email = data_tuple[6]

                    parent.add_widget(update_layout)

            except (Error, TypeError):
                Snackbar(text="Error retrieving database.", duration=2).show()
            except IndexError:
                Snackbar(
                    text="Cannot find registration number {}".format(reg_no), duration=2
                ).show()
        elif len(parent.children) != 0:
            parent.clear_widgets()

    def updateStudentInfo(self, reg_no, parent):
        """
        Gets called when update button is pressed.

        Updates and individual student's data in the database

        :param reg_no: registration number to be updated
        :param parent: Layout from which data to be fetched
        """
        if len(reg_no) == 3:
            widget = parent.children[0]
            fields = ("name", "course", "stream", "batch", "email")
            new_data = (
                widget.name,
                widget.ids.courseBtn.text,
                widget.ids.streamBtn.text,
                widget.batch,
                widget.email,
            )

            try:
                conn = self.connect_database("student_main.db")
                self.update_database(
                    "General_record", conn, fields, new_data, "reg", reg_no
                )
            except Error:
                Snackbar(text="Error updating database.", duration=2).show()
            else:
                Snackbar(
                    text="Updated database for registration number {}".format(reg_no),
                    duration=2,
                ).show()
        else:
            Snackbar(text="Invalid registration number", duration=2).show()

    def populate_admin_info(self, *args):
        """
        Function to populate personal details of admin
        """

        try:
            data_list_admin = self.extractAllData(
                "user_main.db", "admin", order_by="id"
            )[0]
            texts = [
                data_list_admin[1],
                data_list_admin[2],
                str(data_list_admin[5]),
                "",
            ]

            admin = self.ids.adminInfoLayout
            admin.clear_widgets()
            for title, text in zip(
                ["Name", "Email id", "Mobile No.", "Alt. Email Id"], texts
            ):
                admin.add_widget(AdminInfoLabel(title=title, text=text))
        except TypeError:
            pass

    def populate_admin_username(self, *args):
        """
        Function to populate username of admin
        """
        try:
            data_list_admin = self.extractAllData(
                "user_main.db", "admin", order_by="id"
            )[0]

            self.ids.adminUsernameLayout.clear_widgets()
            self.ids.adminUsernameLayout.add_widget(
                AdminInfoLabel(title="Username", text=data_list_admin[3])
            )
        except TypeError:
            pass

    def populate_admin_password(self, *args):
        """
        Function to populate password of admin
        """
        try:
            data_list_admin = self.extractAllData(
                "user_main.db", "admin", order_by="id"
            )[0]
            self.admin_password = data_list_admin[4]
        except TypeError:
            pass

    def populate_not_mail(self, *args):
        """
        Function to populate notification email
        """
        try:
            data_not_mail = self.extractAllData("user_main.db", "admin", order_by="id")[
                0
            ]

            self.ids.notMailLayout.clear_widgets()
            self.ids.notMailLayout.add_widget(
                AdminInfoLabel(title="Notification Email", text=data_not_mail[6])
            )
        except TypeError:
            pass

    def populate_not_mail_password(self, *args):
        """
        Function to populate notification email password
        """
        try:
            data_not_mail = self.extractAllData("user_main.db", "admin", order_by="id")[
                0
            ]
            self.not_mail_password = data_not_mail[7]
        except TypeError:
            pass

    def edit_admin_info(self):
        """
        Adds editable fields to edit personal details of admin
        """
        self.ids.adminInfoEditBtn.icon = "check"
        texts = []
        admin = self.ids.adminInfoLayout
        for each in admin.children[::-1]:
            texts.append(each.children[0].text)

        admin.clear_widgets()
        for hint_text, text in zip(
            ["Name", "Email id", "Mobile No.", "Alt. Email Id"], texts
        ):

            _tmp = AdminInfoEditField()
            _tmp.hint_text = hint_text
            _tmp.text = text
            admin.add_widget(_tmp)

    def show_admin_info(self):
        """
        Adds non-editable fields to show details after editing
        """
        self.ids.adminInfoEditBtn.icon = "pencil"
        texts = []
        admin = self.ids.adminInfoLayout
        for each in admin.children[::-1]:
            texts.append(each.children[0].text)
        # print(texts)

        admin.clear_widgets()
        for title, text in zip(
            ["Name", "Email id", "Mobile No.", "Alt. Email Id"], texts
        ):
            admin.add_widget(AdminInfoLabel(title=title, text=text))

        # Database Addition of name,email,mobile
        fields = ["name", "email", "phone"]
        new_data = texts[: len(texts) - 1]  # not including alt. email for now

        try:
            conn = self.connect_database("user_main.db")
            # READ ME: Here we're supposing that admin table has just one entry with id=1
            self.update_database("admin", conn, fields, new_data, "id", 1)
        except Error:
            Snackbar(text="Error updating admin database", duration=2).show()
        else:
            Snackbar(text="Updated admin details", duration=2,).show()

    def edit_admin_username(self):
        """
        Adds editable fields to edit username of admin
        """
        self.ids.adminUsernameEditBtn.icon = "check"

        username_field = AdminInfoEditField()
        username_field.hint_text = "Username"
        username_field.text = self.ids.adminUsernameLayout.children[0].text

        self.ids.adminUsernameLayout.clear_widgets()
        self.ids.adminUsernameLayout.add_widget(username_field)

    def show_admin_username(self):
        """
        Adds non-editable fields to show details after editing
        """
        self.ids.adminUsernameEditBtn.icon = "pencil"
        self.admin_username = self.ids.adminUsernameLayout.children[0].children[0].text

        self.ids.adminUsernameLayout.clear_widgets()
        self.ids.adminUsernameLayout.add_widget(
            AdminInfoLabel(title="Username", text=self.admin_username)
        )

        # Database manipulation here
        try:
            conn = self.connect_database("user_main.db")
            # READ ME: Here we're supposing that admin table has just one entry with id=1
            self.update_database(
                "admin", conn, "username", self.admin_username, "id", 1
            )
        except Error:
            Snackbar(text="Error updating admin username", duration=2).show()
        else:
            Snackbar(text="Admin username updated", duration=2).show()

    def edit_admin_password(self):
        """
        Adds editable fields to edit password of admin
        """
        self.ids.adminPasswordEditBtn.icon = "check"
        self.ids.eyeBtn.disabled = True
        self.ids.adminPasswordLayout.clear_widgets()

        password_field = AdminInfoEditField()
        password_field.hint_text = "password"
        password_field.text = self.admin_password
        self.ids.adminPasswordLayout.add_widget(password_field)

    flag = 0

    def show_admin_password(self):
        """
        Adds non-editable fields to show details after editing
        """
        self.flag = 1
        self.ids.adminPasswordEditBtn.icon = "pencil"
        self.ids.eyeBtn.disabled = False
        self.admin_password = self.ids.adminPasswordLayout.children[0].children[0].text

        self.ids.adminPasswordLayout.clear_widgets()
        self.admin_pass_label = AdminInfoLabel()
        self.admin_pass_label.title = "Password"
        self.admin_pass_label.text = "*********"
        self.ids.adminPasswordLayout.add_widget(self.admin_pass_label)

        # Database manipulation here
        try:
            conn = self.connect_database("user_main.db")
            # READ ME: Here we're supposing that admin table has just one entry with id=1
            self.update_database("admin", conn, "pass", self.admin_password, "id", 1)
        except Error:
            Snackbar(text="Error updating admin password", duration=2).show()
        else:
            Snackbar(text="Admin password updated", duration=2,).show()

    def edit_not_mail(self):
        """
        Adds editable fields to edit notification email
        """
        self.ids.notMailEditBtn.icon = "check"
        not_mail_field = AdminInfoEditField()
        not_mail_field.hint_text = "Notification Email"
        not_mail_field.text = self.ids.notMailLayout.children[0].text
        self.ids.notMailLayout.clear_widgets()
        self.ids.notMailLayout.add_widget(not_mail_field)

    def show_not_mail(self):
        """
        Adds non-editable fields to show details after editing
        """
        self.ids.notMailEditBtn.icon = "pencil"
        self.not_mail = self.ids.notMailLayout.children[0].children[0].text

        self.ids.notMailLayout.clear_widgets()
        self.ids.notMailLayout.add_widget(
            AdminInfoLabel(title="Notification Email", text=self.not_mail)
        )

        # Database manipulation here
        try:
            conn = self.connect_database("user_main.db")
            # READ ME: Here we're supposing that admin table has just one entry with id=1
            self.update_database("admin", conn, "not_mail", self.not_mail, "id", 1)
        except Error:
            Snackbar(text="Error updating notification email", duration=2).show()
        else:
            Snackbar(text="Notification email updated", duration=2,).show()

    def edit_not_mail_password(self):
        """
        Adds editable fields to edit notification email password
        """
        self.ids.notMailPassEditBtn.icon = "check"
        self.ids.eyeBtn1.disabled = True
        self.ids.notMailPassLayout.clear_widgets()

        mail_pass_field = AdminInfoEditField()
        mail_pass_field.hint_text = "Notification Email password"
        mail_pass_field.text = self.not_mail_password
        self.ids.notMailPassLayout.add_widget(mail_pass_field)

    flag1 = 0

    def show_not_mail_password(self):
        """
        Adds non-editable fields to show details after editing
        """
        self.flag1 = 1
        self.ids.notMailPassEditBtn.icon = "pencil"
        self.ids.eyeBtn1.disabled = False
        self.not_mail_password = self.ids.notMailPassLayout.children[0].children[0].text

        self.ids.notMailPassLayout.clear_widgets()
        self.mail_pass_label = AdminInfoLabel()
        self.mail_pass_label.title = "Notification Email Password"
        self.mail_pass_label.text = "*********"
        self.ids.notMailPassLayout.add_widget(self.mail_pass_label)

        # Database manipulation here
        try:
            conn = self.connect_database("user_main.db")
            # READ ME: Here we're supposing that admin table has just one entry with id=1
            self.update_database(
                "admin", conn, "not_pass", self.not_mail_password, "id", 1
            )
        except Error:
            Snackbar(
                text="Error updating notification email password", duration=2
            ).show()
        else:
            Snackbar(text="Notification email password updated", duration=2,).show()

    def on_eye_btn_pressed(self, inst, key):
        """
        Action to take when eye button is pressed to see passwords
        """
        if key == 1:
            if inst.state == "down":
                self.admin_pass_label.text = self.admin_password
            else:
                self.admin_pass_label.text = "*********"
        elif key == 2:
            if inst.state == "down":
                self.mail_pass_label.text = self.not_mail_password
            else:
                self.mail_pass_label.text = "*********"

    def populate_userslog(self):
        """
        Populates user log screen according user activity
        """
        extracted_logs = extract_log()
        if extracted_logs is not None:
            tmp_data = []
            for each in extracted_logs:
                _tmp = {"dnt": each[1], "uname": each[2], "activity": each[3]}
                tmp_data.append(_tmp)
            self.ids.logList.clear_widgets()
            from custom_widgets import CustomRecycleView

            crv = CustomRecycleView()
            crv.viewclass = "RowUsersLogs"
            self.ids.logList.add_widget(crv)
            crv.data = tmp_data


class ForgotPasswordScreen(Screen, Database):
    """
    Forgot password screen for resetting password for admin
    """

    otp_recieved = "OTP"

    def pre_verify_code(self):
        """
        
        """
        self.ids.codeSubmitBox.clear_widgets()
        self.ids.resetPasswordBox.clear_widgets()
        textfld = MDTextField()
        textfld.hint_text = "Enter OTP"
        textfld.theme_text_color = "Custom"
        textfld.foreground_color = [1, 1, 1, 1]
        t1 = threading.Thread(
            target=self.send_reset_mail, args=(self.ids.codeSubmitBox, textfld)
        )
        t1.start()

    def verify_code(self, inst, *args):
        # print(inst.text, self.otp_recieved)
        if inst.text == str(self.otp_recieved):
            if len(self.ids.resetPasswordBox.children) == 0:
                self.ids.statusLabel.text = ""
                nwpsd_fld = MDTextField()
                nwpsd_fld.hint_text = "New Password"
                nwpsd_fld.password = True
                nwpsd_fld.write_tab = False
                rnwpsd_fld = MDTextField()
                rnwpsd_fld.hint_text = "Re-Enter New Password"
                rnwpsd_fld.password = True
                rnwpsd_fld.write_tab = False
                self.ids.resetPasswordBox.add_widget(nwpsd_fld)
                self.ids.resetPasswordBox.add_widget(rnwpsd_fld)
                anchrl = AnchorLayout()
                anchrl.add_widget(
                    MDRaisedButton(
                        text="Reset Password",
                        on_release=partial(
                            self.new_password_set, nwpsd_fld, rnwpsd_fld
                        ),
                    )
                )
                self.ids.resetPasswordBox.add_widget(anchrl)
                nwpsd_fld.on_text_validate = partial(
                    self.new_password_set, nwpsd_fld, rnwpsd_fld
                )
                rnwpsd_fld.on_text_validate = partial(
                    self.new_password_set, nwpsd_fld, rnwpsd_fld
                )

        else:
            self.ids.statusLabel.text = "OTP doesn't match!"
            self.ids.statusLabel.color = (1, 0, 0, 1)
            self.ids.resetPasswordBox.clear_widgets()

    def new_password_set(self, inst1, inst2, *args):
        if inst1.text == inst2.text:
            if inst1.text != "":
                """
                Database Update
                code here 
                """
                conn = self.connect_database("user_main.db")
                if not self.update_database("admin", conn, "pass", inst1.text, "id", 1):
                    self.ids.codeSubmitBox.clear_widgets()
                    lbl1 = MDLabel(text="Error updating Database")
                    lbl1.color = (1, 0, 0, 1)
                    self.ids.codeSubmitBox.add_widget(lbl1)
                    return

                self.ids.codeSubmitBox.clear_widgets()
                self.ids.sendCodeBox.clear_widgets()
                lbl = MDLabel(text="Password Reset Successfully !")
                lbl.halign = "center"
                lbl.font_size = lbl.width * 0.20
                self.ids.sendCodeBox.add_widget(lbl)
                self.ids.verifnLabel.text = ""
                self.ids.resetPasswordBox.clear_widgets()
                anchrl = AnchorLayout()
                anchrl.add_widget(
                    MDRaisedButton(text="Go to Login", on_release=self.go_to_login)
                )
                self.ids.resetPasswordBox.add_widget(anchrl)
        else:
            self.ids.codeSubmitBox.clear_widgets()
            lbl1 = MDLabel(text="Password Doesn't match!")
            lbl1.color = (1, 0, 0, 1)
            self.ids.codeSubmitBox.add_widget(lbl1)

    def go_to_login(self, *args):
        self.parent.transition = SwapTransition()
        self.parent.parent.opacity = 0.6
        self.parent.current = "login"

    def send_reset_mail(self, Container, textfld, *args):
        """
            Code for send email 
            if email sent return True 
            and status label to be
            set here
        """
        self.ids.sendBtn.disabled = True
        self.ids.statusLabel.color = (1, 1, 1, 1)
        self.ids.statusLabel.text = "Sending..."

        # extract notification mail from database
        data_not_mail = self.extractAllData("user_main.db", "admin", order_by="id")[0]
        not_mail, not_pass = data_not_mail[6:]

        if self.login(not_mail, not_pass):
            # extract admin email
            admin_email = self.extractAllData("user_main.db", "admin", order_by="id")[
                0
            ][2]
            self.otp_recieved = self.send_otp(not_mail, admin_email)
            self.ids.statusLabel.color = (1, 1, 1, 1)
            self.ids.statusLabel.text = "Code Sent"
            self.ids.sendBtn.text = "Resend Code"
            self.ids.sendBtn.disabled = False
            Container.add_widget(textfld)
            Container.add_widget(
                MDRaisedButton(
                    text="Submit", on_release=partial(self.verify_code, textfld)
                )
            )
            textfld.on_text_validate = partial(self.verify_code, textfld)

        else:
            self.mail_sent = False
            self.ids.statusLabel.color = (1, 0, 0, 1)
            self.ids.statusLabel.text = "Error sending mail"
            self.ids.sendBtn.disabled = False

    def login(self, email, password):
        try:
            self.s = smtplib.SMTP("smtp.gmail.com", 587)
            self.s.starttls()
            self.s.login(email, password)
            return True
        except smtplib.SMTPAuthenticationError:
            Snackbar(
                text="Authentication Error: Check notification credentials or turn on less secure app access",
                duration=3,
            ).show()
            return False
        except socket.gaierror:
            Snackbar(
                text="Connection Error: Could not sent mail. Kindly check your connection.",
                duration=2,
            ).show()
            return False
        except Exception:
            Snackbar(
                text="Error sending mail. Check credentials or coonection.", duration=2
            ).show()
            return False

    def send_otp(self, from_, to, *args):
        otp = random.randint(000000, 999999)

        otp_content = """
        Your OTP to reset password for AMS IIIT Kalyani is {}.
        The OTP is valid only for this session.

        This is a system generated email. Kindly do not reply. 
        """
        msg = EmailMessage()
        msg["Subject"] = "Reset Password: AMS IIIT Kalyani"
        msg["From"] = from_
        msg["To"] = to
        try:
            msg.set_content(otp_content.format(otp))
            self.s.send_message(msg)
            return otp
        except Exception as e:
            Snackbar(text="Error sending OTP", duration=1.5).show()
            return None


class ForgotPasswordUser(Screen):
    pass


class NotificationScreen(Screen, Database):
    mail_sending_batch = []

    def openCourseList(self, instance):
        dropdown = CourseDropFee()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def openStreamList(self, instance):
        dropdown = StreamDropFee()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def openCategoryList(self, instance):
        dropdown = CategoryDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def onSelect(self, btn, mainBtn):
        mainBtn.text = btn.text

    def generate_fee_receipt_batch(self, data):
        """
        Fetch From Database and generate pdf
        """
        batch = data["from_year"] + "-" + data["to_year"]
        basic_details = {
            "batch": batch,
            "course": data["course"],
            "stream": data["stream"],
            "sem": data["sem"],
            "due": data["category"],
        }

        if self.ids.rv.data:
            generate_batch_fee_pdf(basic_details, self.ids.rv.data, None)
            Snackbar(text="PDF generated", duration=1.5).show()
            # userlog
            dnt = strftime("%d-%m-%Y %H:%M:%S")
            uname = self.parent.ids.userScreen.user_name
            activity = activities["print_batch_fee"]
            create_log(dnt, uname, activity)
        else:
            Snackbar(text="Empty data!", duration=1.5).show()

    def apply_filter(self, data):
        """
        data should be a dict
        """

        sem = data["sem"] if data["sem"] and int(data["sem"]) > 0 else None
        from_year = (
            data["from_year"]
            if data["from_year"] and int(data["from_year"]) > 0
            else None
        )
        to_year = (
            data["to_year"] if data["to_year"] and int(data["to_year"]) > 0 else None
        )
        course = data["course"] if data["course"] not in ("All", "Course") else None
        stream = data["stream"] if data["stream"] not in ("All", "Stream") else None
        category = data["category"] if data["category"] != "All" else None

        reg_cond = None
        batch_cond = None
        course_cond = None
        stream_cond = None
        cat_cond = None

        if from_year and to_year:
            batch = from_year + "-" + to_year
            batch_cond = 'batch LIKE "' + batch + '%"'
        elif from_year:
            batch_cond = 'batch LIKE "' + from_year + '%"'
        elif to_year:
            batch_cond = 'batch LIKE "%' + to_year + '"'

        if course:
            course_cond = 'course = "' + course + '"'
        if stream:
            stream_cond = 'stream = "' + stream + '"'
        if category:
            cat_cond = 'due > "0"'

        reg_cond = " AND ".join(
            [each for each in [batch_cond, course_cond, stream_cond] if each]
        )

        filtered_list = []
        conn = self.connect_database("student_main.db")

        if reg_cond:
            filtered_list = self.search_from_database_many(
                "General_record", conn, reg_cond
            )

        try:
            # store reg. no. and name
            reg_list = [(each[0], each[1]) for each in filtered_list]

            if sem:
                conn = self.connect_database("fee_main.db")
                self.ids.rv.data = []
                for reg, name in reg_list:
                    try:
                        if cat_cond:
                            tmp_cond = cat_cond + ' AND sem = "' + str(sem) + '"'
                            res = self.search_from_database_many(
                                "_" + str(reg), conn, tmp_cond
                            )[0]
                        else:
                            res = self.search_from_database(
                                "_" + str(reg), conn, "sem", sem, order_by="sem"
                            )[0]

                        x = {
                            "reg": str(reg),
                            "name": name,
                            "paid": str(res[1]),
                            "due": str(res[2]),
                        }
                        self.ids.rv.data.append(x)

                    except (IndexError, TypeError):
                        pass
            else:
                self.ids.rv.data = []
        except (IndexError, TypeError):
            pass

    def openCourseListNotification(self, instance):
        dropdown = CourseDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def openStreamListNotification(self, instance):
        dropdown = StreamDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def openCategoryListNotification(self, instance):
        dropdown = CategoryDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def get_data(self, app):
        """
        Method to get batch details of which student will be notified
        in a list of dictionary.
        """
        if self.check_data():
            if (
                self.ids.notSemester.text != ""
                and self.ids.notFromyear.text != ""
                and self.ids.notToyear.text != ""
                and self.ids.notCourse.text != "Select Course"
                and self.ids.notStream.text != "Select Stream"
            ):
                self.mail_sending_batch.append(
                    {
                        "sem": self.ids.notSemester.text,
                        "fromyear": self.ids.notFromyear.text,
                        "toyear": self.ids.notToyear.text,
                        "course": self.ids.notCourse.text,
                        "stream": self.ids.notStream.text,
                        "category": self.ids.notCategory.text,
                    }
                )

            else:
                Snackbar(text="Something not filled or selected!", duration=0.8).show()

        self.populate_not_data(app)

    def check_data(self):
        """
        Method to check data whether already present or not ! 
        or
        Rescue from same data multiple entry.
        """

        tmp = {
            "sem": self.ids.notSemester.text,
            "fromyear": self.ids.notFromyear.text,
            "toyear": self.ids.notToyear.text,
            "course": self.ids.notCourse.text,
            "category": self.ids.notCategory.text,
            "stream": self.ids.notStream.text,
        }
        if tmp in self.mail_sending_batch:
            Snackbar(text="Duplicate data!", duration=0.8).show()
            return False
        return True

    def mode_selection(self, key):

        if key == 0:
            self.ids.messageMode.clear_widgets()
            self.ids.messageBox.text = ""
            self.ids.height = 0

        elif key == 1:
            self.ids.messageMode.clear_widgets()
            self.ids.messageBox.text = ""
            from custom_layouts import SoftwareModeLayout

            w = SoftwareModeLayout()
            self.ids.messageMode.add_widget(w)

    def delete_data(self, data, app):
        self.mail_sending_batch.remove(data)
        self.populate_not_data(app)

    def populate_not_data(self, app):
        if len(self.mail_sending_batch) == 0:
            self.ids.listLabel.opacity = 0
            self.ids.batchList.clear_widgets()
            l = Label()
            l.text = "No data Added"
            l.color = (
                (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
            )
            self.ids.batchList.add_widget(l)
        else:
            self.ids.batchList.clear_widgets()
            self.ids.listLabel.opacity = 1
            self.ids.batchList.height = len(self.mail_sending_batch) * 36 + 40
            self.ids.notificationContainer.height = (
                880 + len(self.mail_sending_batch) * 36
            )
            from custom_widgets import CustomRecycleView
            from custom_layouts import RowNotification

            w = CustomRecycleView()
            w.viewclass = "RowNotification"
            self.ids.batchList.add_widget(w)
            w.data = self.mail_sending_batch.copy()

    def send_notification(self):
        x = self.ids.batchList.children[0]
        if isinstance(x, CustomRecycleView):
            conn = self.connect_database("student_main.db")
            conn_fee = self.connect_database("fee_main.db")
            mailing_list = []

            for each in x.data:
                cond = (
                    "batch ='"
                    + each["fromyear"]
                    + "-"
                    + each["toyear"]
                    + "' AND course='"
                    + each["course"]
                    + "' AND stream='"
                    + each["stream"]
                    + "'"
                )

                filter1 = self.search_from_database_many("General_record", conn, cond)

                for each_data in filter1:
                    reg = each_data[0]
                    if each["category"] == "All":
                        cond = "sem= '" + each["sem"] + "'"
                    else:
                        cond = "sem= '" + each["sem"] + "' AND due > 0"

                    if self.search_from_database_many("_" + str(reg), conn_fee, cond):
                        mailing_list.append(each_data[6])

            mail_text = self.ids.messageBox.text
            if not mail_text:
                Snackbar(text="Empty message!", duration=0.8).show()
                return

            mailing_list = list(set(mailing_list))
            if not mailing_list:
                Snackbar(text="Mailing list empty!", duration=0.8).show()
                return

            t1 = threading.Thread(
                target=self.send_notif_mail, args=(mail_text, mailing_list)
            )
            t1.start()

        else:
            Snackbar(text="Mailing list empty!", duration=0.8).show()

    def login(self, email, password):
        try:
            self.s = smtplib.SMTP("smtp.gmail.com", 587)
            self.s.starttls()
            self.s.login(email, password)
            return True
        except smtplib.SMTPAuthenticationError:
            Snackbar(
                text="Authentication Error: Check notification credentials or turn on less secure app access",
                duration=3,
            ).show()
            return False
        except socket.gaierror:
            Snackbar(
                text="Connection Error: Could not sent mail. Kindly check your connection.",
                duration=2,
            ).show()
            return False
        except Exception:
            Snackbar(
                text="Error sending mail. Check credentials or coonection.", duration=2
            ).show()
            return False

    def send_notif_mail(self, e_msg, receipients):
        self.ids.sendBtn.text = "Sending..."
        self.ids.sendBtn.disabled = True

        # extract notification mail from database
        data_not_mail = self.extractAllData("user_main.db", "admin", order_by="id")[0]
        not_mail, not_pass = data_not_mail[6:]

        if self.login(not_mail, not_pass):
            msg = EmailMessage()
            msg["Subject"] = "Fee Payment Remainder: IIIT Kalyani"
            msg["From"] = not_mail
            msg["To"] = ",".join(receipients)
            msg.set_content(e_msg)
            try:
                self.s.send_message(msg)
                Snackbar(text="Notification Sent.", duration=1.5).show()
                # userlog
                dnt = strftime("%d-%m-%Y %H:%M:%S")
                uname = self.parent.ids.userScreen.user_name
                activity = activities["send_notification"].format()
                create_log(dnt, uname, activity)
            except Exception as e:
                print(e)
                Snackbar(text="Error sending notification mail", duration=1.5).show()

        self.ids.sendBtn.text = "Send Notification"
        self.ids.sendBtn.disabled = False

    def load_message(self, latefine, duedate):
        msg = """Dear Student,
                    It is informed you that you have not paid
                your tution fee yet.

                    Please,pay your tution fee before {} to
                avoid the extra charges of ₹{}.

                                                    Thanks
                                            """
        self.ids.messageBox.text = msg.format(duedate, latefine)
