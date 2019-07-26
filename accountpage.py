"""
Copyright (c) 2019 Ivanov Yuri

For suggestions and questions:
<kivydevelopment@gmail.com>

This file is distributed under the terms of the same license,
as the Kivy framework.

"""

import os
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivymd.utils.cropimage import crop_image, crop_round_image

if not os.path.exists('user1.png'):
    crop_round_image(
        (int(dp(Window.width * 30 / 100)), int(dp(Window.width * 30 / 100))),
        'user.jpeg',
        'user1.png')


screen_account_page = '''
#:import Window kivy.core.window.Window
#:import MDLabel kivymd.label.MDLabel
#:import MDFillRoundFlatButton kivymd.button.MDFillRoundFlatButton
#:import MDCustomRoundIconButton kivymd.button.MDCustomRoundIconButton
#:import C kivy.utils.get_color_from_hex


#---------------being used in 'Row' Class------------#
<ListItemLayout@BoxLayout>:
    size_hint_y: 1
    canvas:
        Color:
            rgba: (.0,.7,.7,1) if app.theme_cls.theme_style=="Dark" else C("#1B2631")
        RoundedRectangle:
            pos: self.pos
            size: self.size
<LabelForList@Label>:
    color:(0,0,0,1) if app.theme_cls.theme_style=="Dark" else (1,1,1,1)


<Rowinfo@BoxLayout>:
    canvas.before:
        Color:
            rgba:(.0,.7,.7,1) if app.theme_cls.theme_style=="Dark" else C("#17202A")
        RoundedRectangle:
            pos: self.pos
            size: self.size
            
    spacing: "10dp"
    sem:''
    paid: ''
    due: ''
    late:""
    date:''
    remarks:''
   

    #-------paid item--------#
    ListItemLayout:
        size_hint:(0.15,1)
        LabelForList:
            id: lbl0
            text: root.sem
            font_size:"20dp"
            bold: True
    #-------paid item--------#

    ListItemLayout:
        size_hint:(0.15,1)
        LabelForList:
            id: lbl1
            text: root.paid
            font_size:"20dp"
            bold: True

    #-------due item--------#
    ListItemLayout:
        size_hint:(0.15,1)
        LabelForList:
            id: lbl2
            text: root.due
            font_size:"20dp"
            bold: True

    #-------due item--------#
    ListItemLayout:
        size_hint:(0.15,1)
        LabelForList:
            id: lbl3
            text: root.late
            font_size:"20dp"
            bold: True
    #-------due item--------#
    ListItemLayout:
        size_hint:(0.15,1)
        LabelForList:
            id: lbl4
            text: root.date
            font_size:"20dp"
            bold: True

    #-------due item--------#
    ListItemLayout:
        size_hint:(0.25,1)
        LabelForList:
            id: lbl5
            text: root.remarks
            font_size:"20dp"
            bold: True

<LabelAccountPage@Label>
    size_hint: None, None
    size: self.texture_size
    pos_hint: {'center_x': .5}


<BoxMinimumHeight@BoxLayout>
    size_hint_y: None
    height: self.minimum_height

ScreenManager:
    Main:
        id:main
    AccountPage:
        id:info
<Main>:
    name:"main"
    AnchorLayout:
        Button:
            size_hint:.1,.2
            on_release:
                app.root.current="info"

<StudentInfoHeader@BoxLayout>:
    info_title: ''
    info_name: ''

    
    AnchorLayout:
        anchor_x: "right"
        Label:
            size_hint: None, None
            size: self.texture_size
            text: root.info_title
            bold: True
            font_size: sp(15)
    AnchorLayout:
        anchor_x: "left"
        Label:
            text: root.info_name
            size_hint: None, None
            size: self.texture_size

<AccountPage>:
    name: 'info'

    FloatLayout:
        canvas:
            Color:
                rgba:0,0,0,.8
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(5)

            BoxMinimumHeight:
                orientation: 'vertical'
                padding: 0, dp(15), 0, 0
                spacing: dp(7)
                pos_hint: {'top': 1}

                Image:
                    size_hint: None, None
                    size: self.size
                    source: 'user1.png'
                    pos_hint: {'center_x': .5}

                LabelAccountPage:
                    id: name
                    halign: 'center'
                    font_size: '30sp'
                    bold: True
                    #text: "Narendra Damodar Das Modi"

                LabelAccountPage:
                    id: roll
                    halign: 'center'
                    font_size: '18sp'

                    

            BoxLayout:
                id: box
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(10)
                opacity: 0

                canvas.before:
                    Color:
                        rgba: 1, 1, 1, .7
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos

                BoxMinimumHeight:
                    spacing: dp(10)
                    padding: 2, 0, 10, 0

                    BoxLayout:
                        canvas:
                            Color:
                                rgba: 0, 0, 0, .7
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        id: button
                        size_hint_x: None
                        size_hint_y:None
                        height:40


                        StudentInfoHeader:
                            id: course
                            info_title: "Course: "

                        StudentInfoHeader:
                            id: stream
                            info_title: "Stream: "

                        StudentInfoHeader:
                            id: batch
                            info_title: "Batch: "

                        StudentInfoHeader:
                            id: fee
                            info_title: "Fee: "
                            
            
                    MDCustomRoundIconButton:
                        size_hint: None, None
                        size: button.height, button.height
                        source: 'add-friend.png'
                        on_release: root.show_example_snackbar('button')


                BoxLayout:
                    orientation:"vertical"
                    spacing:2
                    BoxLayout:
                        size_hint_y:None
                        height:40
                        canvas:
                            Color:
                                rgba: 0, 0, 0, .7
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos
                        BoxLayout:
                            size_hint:.15,1
                            Label:
                                text:"Semester"
                        BoxLayout:
                            size_hint:.15,1
                            Label:
                                text:"Paid"
                        BoxLayout:
                            size_hint:.15,1
                            Label:
                                text:"Due"
                        BoxLayout:
                            size_hint:.15,1
                            Label:
                                text:"Late"
                        BoxLayout:
                            size_hint:.15,1
                            Label:
                                text:"Date"
                        BoxLayout:
                            size_hint:.25,1
                            Label:
                                text:"Remarks"


                    BoxLayout:
                        canvas:
                            Color:
                                rgba:.6,.3,0.1,0
                            RoundedRectangle:
                                pos:self.pos
                                size:self.size
                        RecycleView:
                            id: rv
                            scroll_type: ['bars', 'content']
                            scroll_wheel_distance: dp(80)
                            bar_width: dp(7)
                            viewclass: 'Rowinfo'
                            data:[{"sem":"1","paid": "2432342", "due": "34242","late":"42334","date":"44-34-3434","remarks":"jaldi do"},{"sem":"2","paid": "24300", "due": "34242","late":"42334","date":"24-04-3434","remarks":"jaldi do"}]
                            RecycleBoxLayout:
                                default_size: None, dp(56)
                                default_size_hint: 1, None
                                size_hint_y: None
                                height: self.minimum_height
                                orientation: "vertical"
                                spacing: dp(5)
                
                        
'''

class ScreenManager(ScreenManager):
    pass
class Main(Screen):
    pass

class AccountPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Window.bind(on_keyboard=self.events_program)

    def on_enter(self, *args):
        Clock.schedule_interval(self.set_button_width, 0)

        self.r= iter(list("39/CSE/17099/297"))
        self.n= iter(list("Narendra Damodar Das Modi"))

        self.b= iter(list("2017-2021"))
        self.c= iter(list("B.Tech"))
        self.s= iter(list("CSE"))
        self.f= iter(list("94700"))

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
        self.ids.info.text = ''

    def set_name_info(self, interval):
        try:
            self.ids.name.text+=next(self.n)  
        except StopIteration:
            pass
            Clock.unschedule(self.set_name_info)

    def set_roll_info(self, interval):
        try:
            self.ids.roll.text += next(self.r)
        except StopIteration:
            pass
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
        self.ids.button.width = \
            Window.width - (dp(50) + self.ids.button.height)

    def show_example_snackbar(self, snack_type):
        """Create and show instance Snackbar for the screen MySnackBar."""

        def callback(instance):    #add to database function
            print(instance.text)
            #toast(instance.text)

        def wait_interval(interval):
            self._interval += interval
            if self._interval > self.my_snackbar.duration:
                anim = Animation(y=dp(10), d=.2)
                anim.start(self.data['Snackbars']['object'].ids.button)
                Clock.unschedule(wait_interval)
                self._interval = 0
                self.my_snackbar = None

        from kivymd.snackbars import Snackbar

        if snack_type == 'simple':
            Snackbar(text="This is a snackbar!").show()
        elif snack_type == 'button':
            Snackbar(text="This is a snackbar", button_text="with a button!",
                     button_callback=callback).show()
        elif snack_type == 'verylong':
            Snackbar(text="This is a very very very very very very very "
                          "long snackbar!").show()
        elif snack_type == 'float':
            if not self.my_snackbar:
                self.my_snackbar = Snackbar(
                    text="This is a snackbar!", button_text='Button',
                    duration=3, button_callback=callback)
                self.my_snackbar.show()
                anim = Animation(y=dp(72), d=.2)
                anim.bind(on_complete=lambda *args: Clock.schedule_interval(
                    wait_interval, 0))
                anim.start(self.data['Snackbars']['object'].ids.button)


    def events_program(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            from kivy.app import App

            App.get_running_app().main_widget.ids.scr_mngr.current = 'previous'
            App.get_running_app().main_widget.ids.toolbar.height = dp(56)

__name__ = "__main__"
class mainApp(App):
    from kivymd.theming import ThemeManager
    theme_cls = ThemeManager()
    theme_cls.theme_style="Light"
    def build(self):
        return Builder.load_string(screen_account_page)
mainApp().run()

