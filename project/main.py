
"""
	
	Account Management System
	Date: 24/02/2019

"""

#imports here
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.core.window import Window, WindowBase
from kivy.animation import Animation
from kivymd.theming import ThemeManager
from kivymd.pickers import MDThemePicker
from kivymd.button import MDRaisedButton
from textfields import MDTextField
import xlrd

import os
from os.path import sep, expanduser, isdir, dirname
from kivy.garden.filebrowser import FileBrowser
from kivy.utils import platform

from database import Database
import re

usernameHash= ''
passwordHash= ''

###########################Global variables##########################
yearNameList=["Ist Year","2nd Year","3rd Year","4th Year"]
txt=[]
#####################################################################
class InfoPopup(ModalView):
	pass
class UserInfoEdit(ModalView):
	pass

class UpdateStudentInfo(ModalView):
	pass

class DeleteWarnPopup(ModalView):
	def onHitConfirm(self):
		#data base part
		#self.ids.label.text="Are you sure to delete year "++" and batch "+
		pass
class CircularToggleButton(BoxLayout,ToggleButton):
	pass

class DropBtn(MDRaisedButton):
	def select(self, instance):
		pass


#dropDown class for Session
class SessionDrop(DropDown):

	def on_open(self):
		pass

	def on_dismiss(self):
		pass

#dropDown class for Course&Stream
class CourseDrop(DropDown):
	pass

#dropDown class for year
class YearDrop(DropDown):
	pass


#sidenav class
class SideNav(ModalView,Database):
	#SessionBtn=ObjectProperty()
	#CourseBtn=ObjectProperty()
	def openSessionList(self,instance):
		dropdown= SessionDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance, btn,self.ids.sessionBtn))

	def openCourseList(self,instance):
		dropdown= CourseDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.courseBtn))

	def openYearList(self,instance):
		dropdown= YearDrop()
		
		if(self.ids.sessionBtn.text=="Current Session"):
			for name in yearNameList:			#yearNameList global variable
				dropBtn= DropBtn(text=name)
				dropBtn.bind(on_release=lambda dropBtn: dropdown.select(dropBtn))
				dropdown.add_widget(dropBtn)

		if(self.ids.sessionBtn.text=="All"):
			table_list= self.findTables("student_main.db")
			for name in table_list:
				years= re.search(".*_(\\d+)_(\\d+)", name)
				txt1=("{}-{}".format(years.group(1), years.group(2)))
				dropBtn= DropBtn(text=txt1)
				dropBtn.bind(on_release=lambda dropBtn: dropdown.select(dropBtn))
				dropdown.add_widget(dropBtn)


		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.yearBtn))
		

	def onSelect(self, inst, btn, mainBtn):
		mainBtn.text= btn.text
		print("Button text=",btn.text)
		if(btn.text=="Current Session"):
			self.ids.yearBtn.text=yearNameList[0]
		if(btn.text=="All"):
			self.ids.yearBtn.text=txt[0]       #txt is global variable(delclared at on_start) for instant action of year btn
		#UserScreen().ids.batchLabel.text=self.ids.courseBtn.text+"\nBatch:"+self.ids.yearBtn.text
		#print(UserScreen().ids.batchLabel.text)
		#print(self.ids.courseBtn.text+"\nBatch:"+self.ids.yearBtn.text)

#popups class
class LoginPopup(ModalView, Database):
	#loginTitle= ObjectProperty()


	'''
	underprocess for keydown login

	def __init__(self, **kwargs):
		super(LoginPopup,self).__init__(**kwargs)
		self._keyboard= Window.request_keyboard(self._on_keyboard_close, self)
		#self._keyboard.bind(on_key_down= self._on_keyboard_down)

	def _on_keyboard_close(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		#self._keyboard.release()
		self.keyboard=None
		print("here")

	def _on_keyboard_down(self, keyboard, keycode, text, modifier):
		#print("herererere")
		print(keycode)
		if(keycode[1]=='enter'):
			self.login()
		return True

	def login(self):
		print("Login Success")
		#self._keyboard.release()
		print(self._keyboard.target)
		#self.keyboard.unbind(on_key_down=self.on_keyboard_down)

	def on_dismiss(self):
		#del self
		#self._keyboard.target=None
		self._on_keyboard_close()

	def on_open(self):
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

	'''

	def login(self, username, password):
		self.username= username
		self.password= password

		#print("username: ", self.username)
		#print("password: ", self.password)

		if(self.username==usernameHash and self.password==passwordHash):
			self.ids.warningInfo.text=""
			self.dismiss()
			return True

		else:
			self.ids.warningInfo.text="Wrong username or password"
			return False

	def show_password(self, field, button):
		field.password = not field.password
		field.focus = True
		button.icon = 'eye' if button.icon == 'eye-off' else 'eye-off'



#ScreenManager Class
class ScreenManager(ScreenManager):
	pass


#HomeScreen Class
class HomeScreen(Screen):
	

	#function to open login popup
	def openLoginPop(self, title):
		lp= LoginPopup()
		lp.ids.loginTitle.text= "{} Login".format(title)
		lp.open()



#UserScreen
class UserScreen(Screen,Database):

	def openSemesterList(self,instance):
		semesterBtn=self.ids.semesterBtn
		dropdown= SemesterDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(btn, self.ids.semesterBtn))

	def onSelect(self, btn, mainBtn):
		mainBtn.text= btn.text
		print(btn.id)

	
	def anim_in(self, instance):
		
		anim= Animation(
				pos_hint={'x':-.3},
				t='in_cubic',
				d=0.3
			)
		anim.start(instance)

	def anim_out(self, instance):
		anim= Animation(
				pos_hint={'x':0},
				t='out_cubic',
				d=0.3
			)
		anim.start(instance)

	def open_sideNav(self):
		sn= SideNav()
		sn.open()



#AdminScreen
class AdminScreen(Screen, Database):
	pc_userName= os.getlogin()

	def onStartAdminScr(self):
		#--------------Update User info Data List ---------------------#
		self.ids.rv.data=[]
		data_list= self.extractAllData("user_all.db", "users")
		for each in data_list:
			x={
			"name": each[1],
			"email": each[2],
			"username": each[3],
			"password": each[4]
			}
			self.ids.rv.data.insert(0,x)

		#print(self.ids.rv.data)
		#--------------------------------------------#

	def change_screen(self, instance):
		if instance.text == 'Manage User':
			self.ids.scrManager.current = 'manageUser'
		elif instance.text == 'Manage Student':
			self.ids.scrManager.current = 'manageStudent'
		elif instance.text=='Admin Setting':
			self.ids.scrManager.current = 'adminSetting'
		elif instance.text=='App Setting':
			self.ids.scrManager.current = 'appSetting'

	def theme_picker_open(self):
		MDThemePicker().open()

	def Add_User_Layout(self):
		target=self.ids.dyn_input
		usr_name=TextInput(size_hint=(.2,1),hint_text="Name",write_tab=False)
		usr_email=TextInput(size_hint=(.2,1),hint_text="E-mail id",write_tab=False)
		usr_username=TextInput(size_hint=(.2,1),hint_text="Username",write_tab=False)
		usr_password=TextInput(size_hint=(.2,1),hint_text="Password")
		usr_submit=MDRaisedButton(size_hint=(.2,1),text="Submit",on_release=lambda x: self.Add_User(usr_name.text,usr_email.text,usr_username.text,usr_password.text))

		target.add_widget(usr_name)
		target.add_widget(usr_email)
		target.add_widget(usr_username)
		target.add_widget(usr_password)
		target.add_widget(usr_submit)

	def Add_User(self,name,email,username,password):
		print(name+" "+email+" "+username+" "+password)

		if(all([not len(each) for each in [name, email,username, password]])):
			print("here")
			return

		self.ids.rv.data.insert(0, {'name': name,'email':email ,'username':username,'password':password })
		self.ids.addusrBtn.state="normal"
		layout=self.ids.dyn_input
		layout.clear_widgets()

		table=	"""
					CREATE TABLE IF NOT EXISTS {} (
					id INTEGER PRIMARY KEY,
					name VARCHAR NOT NULL,
					email VARCHAR NOT NULL,
					username VARCHAR NOT NULL,
					pass VARCHAR NOT NULL
					)
				"""
		data= (name, email, username, password)
		self.addData("user_all.db", table, "users", data)
	def connectFileSelector(self, fromYear, toYear,btntxt):
		if(fromYear=="" or toYear=="" ):
			op=InfoPopup()
			op.ids.label.text="Please fill All required Fields !"
			op.open()
		elif(btntxt=="Select Course"):
			op=InfoPopup()
			op.ids.label.text="Please Select Course !"
			op.open()
		else:
			self.open_FileSelector(fromYear,toYear)

	def open_FileSelector(self, fromYear, toYear):

		#global fromYear
		#fromYear= fromYear

		self.table_name= "year_{}_{}".format(fromYear,toYear)

		if platform == 'win':
			user_path = dirname(expanduser('~')) + sep + 'Documents'
		else:
			user_path = expanduser('~') + sep + 'Documents'
		self._fbrowser = FileBrowser(select_string='Select',favorites=[(user_path, 'Documents')], filters=["*.xls", "*.xlsx"])
		self._fbrowser.bind(on_success=self._fbrowser_success,
							on_canceled=self._fbrowser_canceled)
		global fpopup
		fpopup = Popup(content=self._fbrowser,title_align="center",title="Select File",
						size_hint=(0.7, 0.9), auto_dismiss=True)
		fpopup.open()

	def _fbrowser_canceled(self, instance):
		print ('cancelled, Close self.')
		fpopup.dismiss()


	def _fbrowser_success(self, instance):
		 selected_path= instance.selection[0]
		 fpopup.dismiss()

		 table=	"""
					CREATE TABLE IF NOT EXISTS {} (
					id INTEGER PRIMARY KEY,
					roll_no VARCHAR NOT NULL,
					reg_no INT NOT NULL,
					name VARCHAR NOT NULL
					)
				"""

		 self.readFile("student_main.db", table, self.table_name, selected_path)
		 

	def openEditPopup(self):					#for edit user information open popup
		UserInfoEdit().open()

	#-----------------------select Cousrse---------------------------------------------#
	def openCourseList(self,instance):
		dropdown= CourseDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, (self.ids.courseBtn1)))
	def openCourseList1(self,instance):
		dropdown= CourseDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.courseBtn2))
	def openCourseList2(self,instance):
		dropdown= CourseDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.courseBtn3))

	def openYearList(self,instance):
		dropdown= YearDrop()
		table_list= self.findTables("student_main.db")
		for name in table_list:
			years= re.search(".*_(\\d+)_(\\d+)", name)
			txt1=("{}-{}".format(years.group(1), years.group(2)))
			dropBtn= DropBtn(text=txt1)
			dropBtn.bind(on_release=lambda dropBtn: dropdown.select(dropBtn))
			dropdown.add_widget(dropBtn)

		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.yearBtn))

	def openYearList1(self,instance):
		dropdown= YearDrop()
		table_list= self.findTables("student_main.db")
		for name in table_list:
			years= re.search(".*_(\\d+)_(\\d+)", name)
			txt1=("{}-{}".format(years.group(1), years.group(2)))
			dropBtn= DropBtn(text=txt1)
			dropBtn.bind(on_release=lambda dropBtn: dropdown.select(dropBtn))
			dropdown.add_widget(dropBtn)

		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.yearBtn1))

	def onSelect(self, inst, btn, mainBtn):
		mainBtn.text= btn.text
		print("Button text=",btn.text)
	#-------------------------------------------------------------------#

	def openUStudInfo(self):					#for Update Student information open popup
		if(self.ids.reg_input.text==""):
			op=InfoPopup()
			op.ids.label.text="Please enter Reg. no. !"
			op.open()
		elif(self.ids.yearBtn1.text=="Select Year" or self.ids.courseBtn2.text=="Select Course"):
			op=InfoPopup()
			op.ids.label.text="Please Select All required Buttons !"
			op.open()
		else:
			UpdateStudentInfo().open()

	def openDelWarnPopup(self):
		if(self.ids.yearBtn.text=="Select Year" or self.ids.courseBtn1.text=="Select Course"):
			op=InfoPopup()
			op.ids.label.text="Please Select All required Buttons !"
			op.open()
		else:
			DeleteWarnPopup().open()

#Main App

class AccountManagementSystem(App,Database):
	theme_cls = ThemeManager()
	theme_cls.primary_palette = 'Red'
	theme_cls.theme_style='Light'

	#red_cls=ThemeManager()
	#red_cls.primary_palette = 'Red'

	#green_cls=ThemeManager()
	#green_cls.primary_palette = 'Green'

	def on_start(self):	
		table_list= self.findTables("student_main.db")
		for name in table_list:
			years= re.search(".*_(\\d+)_(\\d+)", name)
			txt.append("{}-{}".format(years.group(1), years.group(2)))

	def build(self):
		return Builder.load_file("gui.kv")



if __name__ == '__main__':

	Window.maximize()
	#Window.size=(900,700)
	Window.minimum_width= 900
	Window.minimum_height=700
	print("window size:",Window.size)
	print(Window.position)

	AccountManagementSystem().run()



