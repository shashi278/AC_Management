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
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.core.window import Window, WindowBase
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.utils import get_color_from_hex as C

from kivymd.theming import ThemeManager
from kivymd.pickers import MDThemePicker
from kivymd.button import MDRaisedButton,MDIconButton
from kivymd.textfields import MDTextField, MDTextFieldRound, MDTextFieldRect
from kivymd.snackbars import Snackbar

import re
import xlrd
import os
from os.path import sep, expanduser, isdir, dirname
from random import choice
from time import sleep

from database import Database
from hoverable import HoverBehavior

usernameHash= ''
passwordHash= ''

#---List  heree-----------------------
from kivymd.selectioncontrols import MDCheckbox,MDSwitch
from kivymd.list import (
    ILeftBody,
    ILeftBodyTouch,
    IRightBodyTouch,
    OneLineIconListItem,
    OneLineListItem,
)
		
#left iconbutton
class ListLeftIconButton(ILeftBodyTouch, MDIconButton):
	pass

#right iconbutton,checkbox,switch
class ListRightIconButton(IRightBodyTouch, MDIconButton):
	pass

class ListRightCheckBox(IRightBodyTouch, MDCheckbox):
	pass

class ListRightSwitch(IRightBodyTouch, MDSwitch):
	pass

#---------------------------------------------------------------------


class InfoPopup(ModalView):
	pass

class ProgressPop(ModalView):
	progress_value= NumericProperty(0)
	progress_total= NumericProperty(0)

class UserInfoEdit(ModalView):
	pass

class UpdateStudentInfo(ModalView):
	pass

class DeleteWarning(ModalView):
	def delete(self):
		'''
		///delete from database code
		'''
		self.ids.container.clear_widgets()
		layout=GridLayout(cols=1)
		self.ids.container.add_widget(layout)
		layout.add_widget(Label(text="Successfully Deleted",font_size=self.height/25+self.width/25))
		anc_layout=AnchorLayout()
		layout.add_widget(anc_layout)
		anc_layout.add_widget(MDRectangleFlatButton(text="Ok",on_release=self.dismiss))
		
	def anim_in(self, instance):
		
		anim= Animation(
				pos_hint={'x':1.4},
				t='in_cubic',
				d=0.3
			)
		anim.start(instance)

	def anim_out(self, instance):
		anim= Animation(
				pos_hint={'x':.6},
				t='out_cubic',
				d=0.3
			)
		anim.start(instance)



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

class HoverLayout(BoxLayout, HoverBehavior):
	pass

class DateInput(MDTextField):

	dd= ''
	mm= ''
	yyyy= ''

	def date_filter(self, substring, do_undo):
		print(substring)
		
		try:
			text= str(int(substring))
			#print("self.text: "+self.text+text)
			#print("cursor: {}".format(self.cursor[0]))
			
			if self.cursor[0] == 0:
				if not len(self.text) :
					self.dd= ''
					self.dd+= text
					return text
				
				elif self.text[0]=="-":
					self.dd= text
					return text

				elif len(self.text)>=2 and self.text[1]=="-":
					self.dd= text+self.dd[1]
					return text

				elif len(self.dd)==1:
					self.dd= text+self.dd
					self.text= self.text+"-"
					self.cursor=(0,0)
					return text

				elif len(self.dd)> len(self.text):
					self.dd= self.dd[0]+text
					self.text= self.text+"-"
					self.cursor=(0,0)
					return text

				#elif len(self.mm)==2 and len(self.yyyy)==4:
					#if self.text[0]=='-':
					return ''


			if self.cursor[0] == 1:
				if len(self.dd)==1 and len(self.text)==1:
					self.dd+= text
					return text+"-"
				elif len(self.dd) > len(self.text):
					self.dd= self.dd[0]+text
					return text+"-"
				else:
					if self.text[1]=="-":
						self.dd= self.dd[0]+text
						return text
					else:
						return ''

			if self.cursor[0]==2:
				if len(self.text)==2:
					return "-"
				else:
					return '-'

			if self.cursor[0]==3:
				if len(self.text)==3:
					self.mm= ''
					self.mm+= text
					return text
				elif len(self.mm)==2:
					self.mm= text+self.mm[1]
					return text
				elif self.text[3]=="-":
					self.mm= text
					return text
				elif len(self.mm)==1:
					self.mm= text+self.mm
					self.text= self.text+"-"
					self.cursor=(3,0)
					return text

			if self.cursor[0]==4:
				if len(self.text)==4:
					if len(self.mm)==2:
						self.mm= self.mm[0]+text
					else:
						self.mm+= text
					return text+"-"
				elif self.text[4]=="-":
					self.mm= self.mm[0]+text
					return text

			if self.cursor[0]==5:
				if len(self.text)==5:
					return "-"
				else:
					return '-'

			if self.cursor[0]>5 and len(self.text)!=10:
				self.yyyy+= text
				return text
			else: return ''





		except Exception as e:
			print(e)
			return ''


class AddDataLayout(ModalView,Database):

	def next_focus(self,text,ele):
		if(ele=="dd" and len(text)==2):
			self.ids.date.ids.mm.focus=True
		if(ele=="mm" and len(text)==2):
			self.ids.date.ids.yy.focus=True
		

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
		print(button.icon)
		field.password = not field.password
		field.focus = True
		button.icon = 'eye' if button.icon == 'eye-off' else 'eye-off'

class ListItemLayout(TouchRippleBehavior, BoxLayout):

	def __init__(self, **kwargs):
		super(ListItemLayout, self).__init__(**kwargs)

	def on_touch_down(self, touch):
		collide_point= self.collide_point(touch.x, touch.y)
		if collide_point:
			self.root= self.parent.parent.parent.parent.parent.parent.parent.parent.manager
			touch.grab(self)
			self.ripple_show(touch)
			return True
		return False

	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)
			self.ripple_fade()
			self.root.ids.profilePage.reg_no= self.parent.ids.lbl1.text
			self.root.transition= RiseInTransition()
			self.root.current= "profilepage"
			return True
		return False

class LabelForList(Label):
	pass

class TextInputForList(TextInput):
	pass

class UserInfo(BoxLayout,Database):

	def edit(self, root, icon, app):
		fields= [child.children[0].text for child in root.children[1:]][::-1]
		print(fields)
		tableName= "users"
		conn= self.connect_database("user_all.db")
		c= conn.execute("select * from {}".format(tableName))
		fields_names= tuple([des[0] for des in c.description][1:])
		#print(fields_names)

		for each,text, fn in zip(root.children[1:][::-1][:],fields, fields_names):
			each.clear_widgets()
			#if user wants to edit
			if icon=="pencil":
				self.color= [.1,.1,.1,1]
				self._temp= TextInputForList()
				self._temp.text= text
				each.add_widget(self._temp)
			else:
				self.color= [.7,.7,.7,1] if app.theme_cls.theme_style=="Dark" else C("#17202A")
				self._temp1= LabelForList()
				self._temp1.font_size="15dp"
				self._temp1.text=text
				each.add_widget(self._temp1)
				#print("In py: {}".format((fn,text,sem)))
				#self.update_database(tableName, conn, fn, text, "sem", sem)


	def delete(self, icon):
		if icon!= "pencil":
			Snackbar(text="Cannot delete while in edit mode. Save ongoing edit first.", duration=2.5).show()

#Being used in profile page
class Rowinfo(BoxLayout, Database):

	color= ListProperty()

	def edit(self, root, icon, app):
		fields= [child.children[0].text for child in root.children[1:]][-2::-1]
		sem= root.children[-1].children[0].text
		print(fields)
		tableName= "_"+str(self.parent.reg_no)
		conn= self.connect_database("fee_main.db")
		c= conn.execute("select * from {}".format(tableName))
		fields_names= tuple([des[0] for des in c.description][1:])
		print(fields_names)

		for each,text, fn in zip(root.children[1:][::-1][1:],fields, fields_names):
			each.clear_widgets()
			#if user wants to edit
			if icon=="pencil":
				self.color= [.1,.1,.1,1]
				self._temp= TextInputForList()
				self._temp.text= text
				each.add_widget(self._temp)
			else:
				self.color= [.7,.7,.7,1] if app.theme_cls.theme_style=="Dark" else C("#17202A")
				self._temp1= LabelForList()
				self._temp1.text=text
				each.add_widget(self._temp1)
				print("In py: {}".format((fn,text,sem)))
				self.update_database(tableName, conn, fn, text, "sem", sem)


	def verify_prev(self, root, icon, app):
		#cannot edit more than one entry at once hence save any already ongoing edit automatically
		for each in root.parent.children:
			if each.ids.btn1.icon!="pencil":
				self.color= [.7,.7,.7,1] if app.theme_cls.theme_style=="Dark" else C("#17202A")
				
				fields= [child.children[0].text for child in each.children[1:]]
				#print(fields)
				for _temp, text in zip(each.children[1:], fields):
					#print(_temp, text)
					_temp.clear_widgets()
					
					_lbl= LabelForList()
					_lbl.text=text
					_temp.add_widget(_lbl)
				each.ids.btn1.icon= "pencil"

	def delete(self, icon):
		if icon!= "pencil":
			Snackbar(text="Cannot delete while in edit mode. Save ongoing edit first.", duration=2.5).show()


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
		'''
		Dynamic search function
		'''
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

	reg_no= 0
	color= StringProperty('')
	colors= ["#C0392B", "#E74C3C", "#9B59B6", "#8E44AD","#2980B9",\
	"#3498DB", "#1ABC9C","#16A085","#27AE60","#2ECC71","#D4AC0D","#F39C12","#E67E22","#D35400"]

	def on_enter(self, *args):
		self.color= choice(self.colors)
		Clock.schedule_interval(self.set_button_width, 0)
		self.extract_data("student_main.db", "General_record")
		self.populate_screen()
		self.ids.rb.reg_no= self.reg_no


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
		self.ids.rv.data=[]

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
		conn= self.connect_database(db_name)

		try:
			self.data_tuple= self.search_from_database(table_name, conn, "reg", self.reg_no)[0]
			self.r= iter(list("Registration Number: {}".format(self.data_tuple[0])))
			self.n= iter(list(self.data_tuple[1]))
			self.b= iter(list(self.data_tuple[4]))
			self.c= iter(list(self.data_tuple[2]))
			self.s= iter(list(self.data_tuple[3]))
			self.f= iter(list(str(self.data_tuple[5])))
			self.totalFee= self.data_tuple[5]
			
		except Exception as e:
			print("Error here: {}".format(e))

	def open_addDataLayout(self):
		AddDataLayout().open()


	def addFeeData(self,ins):
		if(ins.ids.rem.text==""):
			ins.ids.rem.text="NA"
		if(ins.ids.late.text==""):
			ins.ids.late.text="0"

		data_tuple= (int(ins.ids.sem.text), int(ins.ids.paid.text), int(self.totalFee-int(ins.ids.paid.text)),
					int(ins.ids.late.text),ins.ids.date.text,ins.ids.tid.text,ins.ids.rem.text)
		conn= self.connect_database("fee_main.db")

		if self.insert_into_database("_"+str(self.reg_no), conn, data_tuple):

			_temp={
					"sem": str(data_tuple[0]),
					"paid": str(data_tuple[1]),
					"due": str(data_tuple[2]),
					"late": str(data_tuple[3]),
					"date": data_tuple[4],
					"tid": data_tuple[5],
					"remarks": data_tuple[6]
					}

			self.ids.rv.data.append(_temp)

	def populate_screen(self):
		self.ids.rv.data=[]
		# try to populate the screen with data already available in the corresponding
		# reg. no. table
		try:
			data_list= self.extractAllData("fee_main.db", "_"+str(self.reg_no), order_by="sem")
			for data_tuple in sorted(data_list):
				_temp={
					"sem": str(data_tuple[0]),
					"paid": str(data_tuple[1]),
					"due": str(data_tuple[2]),
					"late": str(data_tuple[3]),
					"date": str(data_tuple[4]),
					"tid": data_tuple[5],
					"remarks": data_tuple[6]
				}
				self.ids.rv.data.append(_temp)
		except:
			#else create table
			conn= self.connect_database("fee_main.db")
			if conn is not None:
				with open("fee_record.sql") as table:
					self.create_table(table.read().format("_"+str(self.reg_no)), conn)


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

	def check_edits(self, rowinfo_root):
		_temp= [1 for child in rowinfo_root.children if child.ids.btn1.icon=="check"]
		if len(_temp):
			Snackbar(text="Cannot go back while in edit mode. Save ongoing edits.", duration=2).show()
			return False
		return True



#AdminScreen
class AdminScreen(Screen, Database):
	pc_userName= os.getlogin()

	#will be used to show progress while reading xls
	progress_value=0
	progress_total=0

	def onStartAdminScr(self):
		self.ids.logoutbtn.ids.lbl_txt.text_size= (sp(80), sp(80))
		self.ids.logoutbtn.ids.lbl_txt.font_size= sp(40)

		#--------------Update User info Data List ---------------------#
		self.ids.rv.data=[]
		data_list= self.extractAllData("user_all.db", "users",order_by="id")
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

		if(all([not len(each) for each in [name, email,username, password]])):
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
		try:
			selected_path= instance.selection[0]

			with open("general_record.sql") as table:
				self.readFile("student_main.db", table.read(), "General_record", selected_path, show_progress=True, \
				fromYear= self.fields["fromYear"], toYear= self.fields["toYear"], course= self.fields["course"],\
				stream= self.fields["stream"], fee= self.fields["fee"], fpopup=fpopup)
			fpopup.dismiss()

		except IndexError as e:
			Snackbar(text="Please specify correct file path", duration=2).show()
		 

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
			op.ids.label.text="Please enter Reg. no"
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
			op.ids.label.text="Please Select All required Buttons."
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
	Window.minimum_width= 900
	Window.minimum_height=700

	AccountManagementSystem().run()
