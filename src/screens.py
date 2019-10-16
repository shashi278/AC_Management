from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.popup import Popup

from kivymd.uix.button import (
    MDRaisedButton,
    MDRectangleFlatButton,
    MDFloatingActionButton,
)
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDThemePicker

import os
from os.path import sep, expanduser, isdir, dirname
from random import choice
from sqlite3 import Error

from database import Database
from popups import LoginPopup, DeleteWarning, SideNav, AddDataLayout
from custom_layouts import UpdateStudentLayout
from dropdowns import *

# ScreenManager Class
class ScreenManager(ScreenManager):
    pass


# HomeScreen Class
class HomeScreen(Screen):

    # function to open login popup
    def openLoginPop(self, title):
        lp = LoginPopup()
        lp.ids.loginTitle.text = "{} Login".format(title)
        lp.open()


# UserScreen
class UserScreen(Screen, Database):
    def onStartUserScr(self):

        # should be fixed inside MDIconButton in md library itself
        self.ids.hamburger.ids.lbl_txt.text_size = (sp(80), sp(80))
        self.ids.hamburger.ids.lbl_txt.font_size = sp(60)
        self.ids.search.text = ""

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
        except:
            pass

    def openSemesterList(self, instance):
        semesterBtn = self.ids.semesterBtn
        dropdown = SemesterDrop()
        dropdown.open(instance)
        dropdown.bind(
            on_select=lambda instance, btn: self.onSelect(btn, self.ids.semesterBtn)
        )

    def onSelect(self, btn, mainBtn):
        mainBtn.text = btn.text
        print(btn.id)

    def anim_in(self, instance):

        anim = Animation(pos_hint={"x": -0.3}, t="in_cubic", d=0.3)
        anim.start(instance)

    def anim_out(self, instance):
        anim = Animation(pos_hint={"x": 0}, t="out_cubic", d=0.3)
        anim.start(instance)

    def open_sideNav(self):
        sn = SideNav()
        sn.open()

    def search(self, text):
        """
		Dynamic search function
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
        self.color = choice(self.colors)
        Clock.schedule_interval(self.set_button_width, 0)
        self.extract_data("student_main.db", "General_record")
        self.populate_screen()
        self.ids.rb.reg_no = self.reg_no

        Clock.schedule_interval(self.set_name_info, 0)
        Clock.schedule_interval(self.set_roll_info, 0)
        Clock.schedule_once(self.schedule, 0.5)

        Animation(opacity=1, d=0.5).start(self.ids.box)

    def schedule(self, interval):
        Clock.schedule_interval(self.set_course_info, 0.01)
        Clock.schedule_interval(self.set_stream_info, 0.01)
        Clock.schedule_interval(self.set_batch_info, 0.01)
        Clock.schedule_interval(self.set_fee_info, 0.01)

    def on_leave(self, *args):
        self.ids.name.text = ""
        self.ids.roll.text = ""
        self.ids.course.info_name = ""
        self.ids.stream.info_name = ""
        self.ids.batch.info_name = ""
        self.ids.fee.info_name = ""
        self.ids.rv.data = []

    def set_name_info(self, interval):
        try:
            self.ids.name.text += next(self.n)
        except StopIteration:
            Clock.unschedule(self.set_name_info)

    def set_roll_info(self, interval):
        try:
            self.ids.roll.text += next(self.r)
        except StopIteration:
            Clock.unschedule(self.set_roll_info)

    def set_course_info(self, interval):
        try:
            self.ids.course.info_name += next(self.c)
        except StopIteration:
            Clock.unschedule(self.set_course_info)

    def set_stream_info(self, interval):
        try:
            self.ids.stream.info_name += next(self.s)
        except StopIteration:
            Clock.unschedule(self.set_stream_info)

    def set_batch_info(self, interval):
        try:
            self.ids.batch.info_name += next(self.b)
        except StopIteration:
            Clock.unschedule(self.set_batch_info)

    def set_fee_info(self, interval):
        try:
            self.ids.fee.info_name += next(self.f)
        except StopIteration:
            Clock.unschedule(self.set_fee_info)

    def set_button_width(self, interval):
        self.ids.button.width = Window.width - (dp(50) + self.ids.button.height)

    def extract_data(self, db_name, table_name):
        conn = self.connect_database(db_name)

        try:
            self.data_tuple = self.search_from_database(
                table_name, conn, "reg", self.reg_no
            )[0]
            self.r = iter(list("Registration Number: {}".format(self.data_tuple[0])))
            self.n = iter(list(self.data_tuple[1]))
            self.b = iter(list(self.data_tuple[4]))
            self.c = iter(list(self.data_tuple[2]))
            self.s = iter(list(self.data_tuple[3]))
            self.f = iter(list(str(self.data_tuple[5])))
            self.totalFee = self.data_tuple[5]

        except Exception as e:
            print("Error here: {}".format(e))

    def open_addDataLayout(self):
        AddDataLayout().open()

    def addFeeData(self, ins):
        if ins.ids.rem.text == "":
            ins.ids.rem.text = "NA"
        if ins.ids.late.text == "":
            ins.ids.late.text = "0"

        data_tuple = (
            int(ins.ids.sem.text),
            int(ins.ids.paid.text),
            int(self.totalFee - int(ins.ids.paid.text)),
            int(ins.ids.late.text),
            ins.ids.date.text,
            ins.ids.tid.text,
            ins.ids.rem.text,
        )
        conn = self.connect_database("fee_main.db")

        if self.insert_into_database("_" + str(self.reg_no), conn, data_tuple):

            _temp = {
                "sem": str(data_tuple[0]),
                "paid": str(data_tuple[1]),
                "due": str(data_tuple[2]),
                "late": str(data_tuple[3]),
                "date": data_tuple[4],
                "tid": data_tuple[5],
                "remarks": data_tuple[6],
            }

            self.ids.rv.data.append(_temp)

    def populate_screen(self):
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

    def anim_in(self, instance):

        anim = Animation(pos_hint={"y": -0.3}, t="in_cubic", d=0.3)
        anim.start(instance)

    def anim_out(self, instance):
        anim = Animation(pos_hint={"y": 0}, t="out_cubic", d=0.3)
        anim.start(instance)

    def check_edits(self, rowinfo_root):
        _temp = [1 for child in rowinfo_root.children if child.ids.btn1.icon == "check"]
        if len(_temp):
            Snackbar(
                text="Cannot go back while in edit mode. Save ongoing edits.",
                duration=2,
            ).show()
            return False
        return True


# AdminScreen
class AdminScreen(Screen, Database):
    pc_userName = os.getlogin()

    # will be used to show progress while reading xls
    progress_value = 0
    progress_total = 0

    def onStartAdminScr(self):

        self.ids.logoutbtn.ids.lbl_txt.text_size = (sp(80), sp(80))
        self.ids.logoutbtn.ids.lbl_txt.font_size = sp(40)

        # --------------Update User info Data List ---------------------#
        self.ids.rv.data = []
        data_list = self.extractAllData("user_main.db", "users", order_by="id")
        for counter, each in enumerate(data_list, 1):
            x = {
                "sno": str(counter),
                "name": each[1],
                "email": each[2],
                "username": each[3],
                "password": each[4],
            }
            self.ids.rv.data.append(x)
        # --------------------------------------------#

    def change_screen(self, instance):
        if instance.text == "Manage User":
            self.ids.scrManager.current = "manageUser"
        elif instance.text == "Manage Student":
            self.ids.scrManager.current = "manageStudent"
        elif instance.text == "Admin Setting":
            self.ids.scrManager.current = "adminSetting"
        elif instance.text == "App Setting":
            self.ids.scrManager.current = "appSetting"

    def theme_picker_open(self):
        MDThemePicker().open()

    def Add_User_Layout(self):
        target = self.ids.dyn_input
        usr_name = TextInput(size_hint=(0.2, 1), hint_text="Name", write_tab=False)
        usr_email = TextInput(
            size_hint=(0.2, 1), hint_text="E-mail id", write_tab=False
        )
        usr_username = TextInput(
            size_hint=(0.2, 1), hint_text="Username", write_tab=False
        )
        usr_password = TextInput(
            size_hint=(0.2, 1), hint_text="Password", write_tab=False
        )
        usr_submit = MDRaisedButton(
            size_hint=(0.2, 1),
            text="Submit",
            on_release=lambda x: self.Add_User(
                usr_name.text, usr_email.text, usr_username.text, usr_password.text
            ),
        )

        target.add_widget(usr_name)
        target.add_widget(usr_email)
        target.add_widget(usr_username)
        target.add_widget(usr_password)
        target.add_widget(usr_submit)

    def Add_User(self, name, email, username, password):

        if all([not len(each) for each in [name, email, username, password]]):
            return

        self.ids.rv.data.append(
            {"name": name, "email": email, "username": username, "password": password},
        )
        self.ids.addusrBtn.state = "normal"
        layout = self.ids.dyn_input
        layout.clear_widgets()

        data = (name, email, username, password)
        with open("user_record.sql", "r") as table:
            self.addData("user_main.db", table.read(), "users", data)

    def connectFileSelector(self, fromYear, toYear, course, stream, fee):
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
        global fpopup
        fpopup = Popup(
            content=self._fbrowser,
            title_align="center",
            title="Select File",
            size_hint=(0.7, 0.9),
            auto_dismiss=False,
        )
        fpopup.open()

    def _fbrowser_canceled(self, instance):
        fpopup.dismiss()

    def _fbrowser_success(self, instance):
        try:
            selected_path = instance.selection[0]

            with open("general_record.sql") as table:
                self.readFile(
                    "student_main.db",
                    table.read(),
                    "General_record",
                    selected_path,
                    fromYear=self.fields["fromYear"],
                    toYear=self.fields["toYear"],
                    course=self.fields["course"],
                    stream=self.fields["stream"],
                    fee=self.fields["fee"],
                    fpopup=fpopup,
                )
            fpopup.dismiss()

        except IndexError as e:
            Snackbar(text="Please specify a valid file path", duration=2).show()

    # -----------------------select Cousrse and Stream---------------------------------------------#
    def openCourseList(self, instance):
        dropdown = CourseDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def openStreamList(self, instance):
        dropdown = StreamDrop()
        dropdown.open(instance)
        dropdown.bind(on_select=lambda instance_, btn: self.onSelect(btn, instance))

    def onSelect(self, btn, mainBtn):
        mainBtn.text = btn.text

    def deleteBatch(self, fromYear, toYear, course, stream):
        if fromYear == "" or toYear == "":
            Snackbar(text="Please fill in all required fields.", duration=2).show()

        elif course == "Select Course":
            Snackbar(text="Please select a course.", duration=2).show()

        elif stream == "Select Stream":
            Snackbar(text="Please select a stream.", duration=2).show()

        else:
            # print(fromYear, toYear, course, stream)
            data = {
                "fromYear": fromYear,
                "toYear": toYear,
                "course": course,
                "stream": stream,
            }
            DeleteWarning("batch", data, "student_main.db", "General_record").open()

    def checkBeforeUpdate(self, reg_no, parent):
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
        if len(reg_no) == 3:
            widget = parent.children[0]
            fields = ("name", "course", "stream", "batch")
            new_data = (
                widget.name,
                widget.ids.courseBtn.text,
                widget.ids.streamBtn.text,
                widget.batch,
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
