
"""
	
	Account Management System
	Date: 24/02/2019

"""

#imports here
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen,RiseInTransition
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
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.garden.filebrowser import FileBrowser
from kivy.utils import platform

from kivymd.theming import ThemeManager
from kivymd.pickers import MDThemePicker
from kivymd.button import MDRaisedButton
from kivymd.textfields import MDTextField

import re
import xlrd
import os
from os.path import sep, expanduser, isdir, dirname

from database import Database

usernameHash= ''
passwordHash= ''

class InfoPopup(ModalView):
	pass

class UserInfoEdit(ModalView):
	pass

class UpdateStudentInfo(ModalView):
	pass

class DeleteWarnPopup(ModalView):
	def onHitConfirm(self):
		pass


class CircularToggleButton(BoxLayout,ToggleButton):
	pass

class DropBtn(MDRaisedButton):
	def select(self, instance):
		pass


#dropDown class for Session
class SessionDrop(DropDown):
	pass

#dropDown class for Course&Stream
class CourseDrop(DropDown):
	pass

class StreamDrop(DropDown):
	pass

#dropDown class for year
class YearDrop(DropDown):
	pass


#sidenav class
class SideNav(ModalView,Database):
	pass
		
class AddDataLayout(ModalView,Database):
	pass
#popups class
class LoginPopup(ModalView, Database):

	def login(self, username, password):
		self.username= username
		self.password= password

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

class ListItemLayout(TouchRippleBehavior, BoxLayout):

	def __init__(self, **kwargs):
		super(ListItemLayout, self).__init__(**kwargs)

	def on_touch_down(self, touch):
		collide_point= self.collide_point(touch.x, touch.y)
		if collide_point:
			#print("touched down")
			self.root= self.parent.parent.parent.parent.parent.parent.parent.parent.manager
			touch.grab(self)
			self.ripple_show(touch)
			return True
		return False

	def on_touch_up(self, touch):
		if touch.grab_current is self:
			#print("touched up")
			touch.ungrab(self)
			self.ripple_fade()
			self.root.ids.profilePage.reg_no= self.parent.ids.lbl1.text
			self.root.transition= RiseInTransition()
			self.root.current= "profilepage"
			return True
		return False

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

	def onStartUserScr(self):

		#should be fixed inside MDIconButton in md library itself
		self.ids.hamburger.ids.lbl_txt.text_size= (sp(80), sp(80))
		self.ids.hamburger.ids.lbl_txt.font_size= sp(60)

		self.ids.search.text=''

		#--------------Update Student list---------------------#
		self.ids.rv.data=[]
		try:
			data_list= self.extractAllData("student_main.db", "General_record")
			for counter, each in enumerate(data_list,1):
				x={
				"sno": counter,
				"reg": each[0],
				"name": each[1],
				"course": each[2],
				"stream": each[3],
				"batch": each[4]
				}
				self.ids.rv.data.append(x)
		except:
			pass

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

	def search(self, text):
		print(text)
		if not text:
			self.onStartUserScr()
			return

		filtered_list= []
		conn= self.connect_database("student_main.db")

		try:
			text= int(text)
			prop_list= ["reg",] if len(str(text))<4 else ["reg", "batch"]

		except:
			prop_list=["stream", "course", "name", "batch"]

		for prop in prop_list:
			filtered_list.extend(self.search_from_database("General_record", conn, prop, text))
		
		self.populate_on_search( sorted(list(set(filtered_list))) )




	def populate_on_search(self, filtered_list):
		self.ids.rv.data=[]

		for counter, each in enumerate(filtered_list,1):
			x={
				"sno": counter,
				"reg": each[0],
				"name": each[1],
				"course": each[2],
				"stream": each[3],
				"batch": each[4]
				}
			self.ids.rv.data.append(x)

#ProfilePage
class ProfilePage(Screen, Database):

	reg_no=0

	def on_enter(self, *args):
		Clock.schedule_interval(self.set_button_width, 0)
		self.extract_data("student_main.db", "General_record")

		Clock.schedule_interval(self.set_name_info, 0)
		Clock.schedule_interval(self.set_roll_info, 0)
		Clock.schedule_once(self.schedule,0.5)

		Animation(opacity=1, d=.5).start(self.ids.box)

	def schedule(self, interval):
		Clock.schedule_interval(self.set_course_info, 0.01)
		Clock.schedule_interval(self.set_stream_info, 0.01)
		Clock.schedule_interval(self.set_batch_info, 0.01)
		Clock.schedule_interval(self.set_fee_info, 0.01)

	def on_leave(self, *args):
		self.ids.name.text=''
		self.ids.roll.text=''
		self.ids.course.info_name=''
		self.ids.stream.info_name=''
		self.ids.batch.info_name=''
		self.ids.fee.info_name=''

	def set_name_info(self, interval):
		try:
			self.ids.name.text+=next(self.n)
		except StopIteration:
			Clock.unschedule(self.set_name_info)

	def set_roll_info(self, interval):
		try:
			self.ids.roll.text += next(self.r)
		except StopIteration:
			Clock.unschedule(self.set_roll_info)

	def set_course_info(self, interval):
		try:
			self.ids.course.info_name+=next(self.c)
		except StopIteration:
			Clock.unschedule(self.set_course_info)

	def set_stream_info(self, interval):
		try:
			self.ids.stream.info_name+=next(self.s)
		except StopIteration:
			Clock.unschedule(self.set_stream_info)

	def set_batch_info(self, interval):
		try:
			self.ids.batch.info_name+=next(self.b)
		except StopIteration:
			Clock.unschedule(self.set_batch_info)

	def set_fee_info(self, interval):
		try:
			self.ids.fee.info_name+=next(self.f)
		except StopIteration:
			Clock.unschedule(self.set_fee_info)

	def set_button_width(self, interval):
		self.ids.button.width = Window.width - (dp(50) + self.ids.button.height)

	def extract_data(self, db_name, table_name):
		conn= self.connect_database("student_main.db")

		try:
			data_tuple= self.search_from_database(table_name, conn, "reg", self.reg_no)[0]
			self.r= iter(list("Registration Number: {}".format(data_tuple[0])))
			self.n= iter(list(data_tuple[1]))
			self.b= iter(list(data_tuple[4]))
			self.c= iter(list(data_tuple[2]))
			self.s= iter(list(data_tuple[3]))
			self.f= iter(list(str(data_tuple[5])))
			self.totalFee= data_tuple[5]
			
		except:
			pass

	def open_addDataLayout(self):
		AddDataLayout().open()


	def addFeeData(self,ins):
		if(ins.ids.rem.text==""):
			ins.ids.rem.text="NA"
		if(ins.ids.late.text==""):
			ins.ids.late.text="0"
		self.ids.rv.data.append({"sem":ins.ids.sem.text,\
									"paid": "₹ "+ins.ids.paid.text, \
									"due": "₹ "+str(self.totalFee-int(ins.ids.paid.text)), \
									"late": "₹ "+ins.ids.late.text,\
									"date":ins.ids.date.text, \
									"remarks":ins.ids.rem.text})



	def anim_in(self, instance):
		
		anim= Animation(
				pos_hint={'y':-.3},
				t='in_cubic',
				d=0.3
			)
		anim.start(instance)

	def anim_out(self, instance):
		anim= Animation(
				pos_hint={'y':0},
				t='out_cubic',
				d=0.3
			)
		anim.start(instance)




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
		usr_submit=MDRaisedButton(size_hint=(.2,1),text="Submit",on_release=lambda x: \
			self.Add_User(usr_name.text,usr_email.text,usr_username.text,usr_password.text))

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


	def connectFileSelector(self, fromYear, toYear, course, stream, fee):
		if(fromYear=="" or toYear=="" or fee==""):
			op=InfoPopup()
			op.ids.label.text="Please fill in all required fields."
			op.open()

		elif(course=="Select Course"):
			op=InfoPopup()
			op.ids.label.text="Please Select Course."
			op.open()
		elif(stream=="Select Stream"):
			op=InfoPopup()
			op.ids.label.text="Please Select Stream."
			op.open()
		else:
			self.fields= {
						"fromYear": fromYear,
						"toYear": toYear,
						"course": course,
						"stream": stream,
						"fee": fee
						}	
			self.open_FileSelector()

	def open_FileSelector(self):

		if platform == 'win':
			user_path = dirname(expanduser('~')) + sep + 'Documents'
		else:
			user_path = expanduser('~') + sep + 'Documents'
		self._fbrowser = FileBrowser(select_string='Select',favorites=[(user_path, 'Documents')], filters=["*.xls", "*.xlsx"])
		self._fbrowser.bind(on_success=self._fbrowser_success,
							on_canceled=self._fbrowser_canceled)
		global fpopup
		fpopup = Popup(content=self._fbrowser,title_align="center",title="Select File",
						size_hint=(0.7, 0.9), auto_dismiss=False)
		fpopup.open()

	def _fbrowser_canceled(self, instance):
		print ('cancelled, Close self.')
		fpopup.dismiss()


	def _fbrowser_success(self, instance):
		 selected_path= instance.selection[0]
		 fpopup.dismiss()

		 with open("general_record.sql") as table:
		 	self.readFile("student_main.db", table.read(), "General_record", selected_path, \
		 		fromYear= self.fields["fromYear"], toYear= self.fields["toYear"], course= self.fields["course"],\
		 		stream= self.fields["stream"], fee= self.fields["fee"])
		 

	def openEditPopup(self):					#for edit user information open popup
		UserInfoEdit().open()

	#-----------------------select Cousrse---------------------------------------------#
	def openCourseList1(self,instance):
		dropdown= CourseDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.courseBtn1))
	def openCourseList2(self,instance):
		dropdown= CourseDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.courseBtn2))
	

	def openStreamList1(self,instance):
		dropdown= StreamDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.streamBtn1))

	def openStreamList2(self,instance):
		dropdown= StreamDrop()
		dropdown.open(instance)
		dropdown.bind(on_select=lambda instance, btn: self.onSelect(instance,btn, self.ids.streamBtn2))


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
	#theme_cls.primary_palette = 'Blue'
	#theme_cls.theme_style='Light'
	#theme_cls.accent_hue= "500"

	def build(self):
		return Builder.load_file("gui.kv")



if __name__ == '__main__':

	Window.maximize()
	#Window.size=(900,700)
	Window.minimum_width= 900
	Window.minimum_height=700

	AccountManagementSystem().run()
