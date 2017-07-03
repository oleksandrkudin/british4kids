"""redirect debugging information from Android via USB to PC: adb  logcat python *:s
"""

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar
from kivy.uix.checkbox import CheckBox
from kivy.base import runTouchApp
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from plyer import tts
from kivy.graphics import Rectangle, Color
from kivy.core.text import Label as CoreLabel
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
#from components.ttsspeak import TtsSpeak
#from ttsspeak import TtsSpeak
#kivy.require('1.0.7')
from kivy.utils import platform

from functools import partial

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty

import time
import os.path
import pickle
import lesson
from student import *
import learningmaterials
import random

from array import array

catalog = learningmaterials.catalog

class ButtonImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ButtonImage, self).__init__(**kwargs)

class MemoryCard (ButtonImage):
    def __init__ (self, **kwargs):
        self.back_image = kwargs.pop('back_image')
        self.front_image = kwargs.pop('front_image')
        self.languageitem = kwargs.pop('languageitem')
        self.card_type = kwargs.pop('card_type')
        self.card_side = 'back'
        self.active = True
        kwargs['source'] = self.back_image

        if self.card_type == 'text':
                my_text = CoreLabel(text=self.languageitem, font_size=24, bold=True, color=[1,1,1,1])
                my_text.refresh()
                texture = my_text.texture
        if self.card_type == 'picture':
                my_img = CoreImage (self.front_image)
                texture = my_img.texture
        self.front_texture = texture

        my_img = CoreImage (self.back_image)
        self.back_texture = my_img.texture
        
        super(ButtonImage, self).__init__(**kwargs)
    def on_press (self):
        if self.active:
            sm.screens[4].game.play(self)
    def flip (self):

        
        if self.card_side == 'back':
            #self.canvas.clear()
            
            self.texture = self.front_texture
            self.card_side = 'front'  
        elif self.card_side == 'front':
            self.source = self.back_image
            self.card_side = 'back'
            #self.reload()
            self.texture = self.back_texture
        #print ('texture.size:',self.texture.size)
    def equal (self, card):
        if card:
            if self.languageitem == card.languageitem:
                return True
        return False

class FlashCard (ButtonImage):
    def __init__ (self, **kwargs):
        self.image = kwargs.pop('image')
        self.languageitem = kwargs.pop('languageitem')
        kwargs['source'] = self.image
        super(ButtonImage, self).__init__(**kwargs)

class MemoryButton (ButtonImage):
    def __init__ (self, **kwargs):
        self.image = kwargs.pop('image')
        self.languageitem = kwargs.pop('languageitem')
        kwargs['source'] = self.image
        super(MemoryButton, self).__init__(**kwargs)
        self.selected = False
    def click (self):
        if self.selected:
            self.selected = False
            self.reload()
            
        else:
            self.selected = True
            #arr = array('B', [int((pixel if type(pixel) == int else ord(pixel)) * 0.6) for pixel in  self.texture.pixels])
            arr = array('B',  self.texture.pixels)
            for i in range(self.texture.size[0] * self.texture.size[1]):
                index = (i+1)*4-1
                arr[index] = int(arr[index]*0.3)
            texture = Texture.create(size=self.texture.size, colorfmt='rgba')
            texture.blit_buffer ( arr, colorfmt='rgba', bufferfmt='ubyte' )
            texture.flip_vertical()
            self.texture = texture
            
                
    def on_press (self):
        #self.click()
        sm.screens[5].game.on_press(self)

       

class MyImage (Image):
    pass

class MyButtonVideo(ButtonBehavior, Video):
    def __init__(self, **kwargs):
        super(MyButtonVideo, self).__init__(**kwargs)
        #self.source = kwargs['source']
        #self.volume = 0.5
        #self.play = kwargs['state']
        #self.state = 'play'
        #self.loaded = True
        #self.eos = 'loop'


class ImageLabel (AnchorLayout):
   def __init__(self, **kwargs):
       image = kwargs.pop('image')
       languageitem = kwargs.pop('languageitem')
       font_size = kwargs.pop('font_size')
       color=kwargs.pop('color')

       text_kwargs = {}
       if font_size: text_kwargs['font_size'] = font_size
       if color: text_kwargs['color'] = color
       if 'bold' in kwargs: text_kwargs['bold'] = kwargs.pop('bold')
       
       AnchorLayout.__init__(self,**kwargs)
       self.image = Image (source = image)
       self.label = Label (text = languageitem, **text_kwargs)
       self.add_widget (self.image)
       self.add_widget (self.label)

def two_way_generator (seq):
    i=0
    x=1
    m_len = len(seq)
    while True:
        x = yield (seq[i])
        i = (i+x) % m_len


#icon: 'data/images/wrong.png'

Builder.load_string("""
<StudentsScreen>:
    id: student_screen
    GridLayout:
        id: student_layout    
        cols: 1
        spacing: 20, 20
        padding: [20, 0, 20, 0]
        ButtonImage:
            source: 'data/sophia.jpg'
            on_press: root.init_student('Sophia')
        ButtonImage:   
            source: 'data/olya.jpg'
            on_press: root.init_student('Olya')
        ButtonImage:
            source: 'data/images/oleksandr.png'
            on_press: root.init_student('Oleksandr')
<ScenariosScreen>:
    id: scenario_screen
    GridLayout:
        cols: 2
        spacing: 20, 20
        padding: [20, 0, 20, 0]
        ButtonImage:
            source: 'data/flashcards.jpg'
            on_press: root.set_scenario ('vocabulary')
        ButtonImage:
            source: 'data/stories.jpg'
            on_press: root.set_scenario ('stories')
        ButtonImage:
            source: 'data/conversations.png'
            on_press: root.set_scenario ('dialogs')
        ButtonImage:
            source: 'data/images/memory.jpg'
            on_press: root.set_scenario ('memory')
        ButtonImage:
            source: 'data/images/remember.jpg'
            on_press: root.set_scenario ('remember')
        ButtonImage:
            source: 'data/images/interaction.png'
            on_press: root.set_scenario ('interactions')
            
            
<VocabularyScreen>:
    id: vocabulary_screen     
                      
                
<DetailsScreen>:
    GridLayout:
        cols: 1
        rows: 4
        ActionBar: 
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'Learning English for Kids!'
                    with_previous: False
                    on_press: root.manager.current = 'students'
                    app_icon: 'data/images/home5.png'
                ActionButton:
                    id: btn_wrong
                    on_press: root.press_wrong()
                ActionButton:
                    id: btn_correct
                    icon: 'data/images/checkmark.png'
                    on_press: root.press_correct()
                ActionButton:
                    id: btn_help
                    icon: 'data/images/questionmark.png'
                    on_press: root.press_help()
                ActionOverflow:
                ActionButton:
                    text: 'Btn0'
                    icon: 'atlas://data/images/defaulttheme/audio-volume-high'
                    on_press: root.sound_li()
                ActionGroup:
                    ActionButton:
                        text: 'Btn6'
                        icon: 'atlas://data/images/defaulttheme/overflow'
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'
            Image:
                id: word_image 
                allow_stretch: True
                keep_ratio: True
        RelativeLayout:
            size_hint: 1, 0.1
            Label:
                id: word_text
                font_size: '25sp'
                text: ''
        RelativeLayout:
            size_hint: 1, 0.15
            AnchorLayout:
                anchor_x: 'left'
                ButtonImage:
                    id: btn_prev
                    size_hint: 0.15, 1
                    source: 'data/images/prev.png'
                    on_press: root.play_next_card(-1)
            AnchorLayout:
                anchor_x: 'right'
                ButtonImage:
                    id: btn_next
                    size_hint: 0.15, 1
                    source: 'data/images/next.png'
                    on_press: root.play_next_card(1)

<MemoryScreen>:
    id: memory_screen
    GridLayout:
        cols: 1
        rows: 2
        ActionBar: 
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'Learning English for Kids!'
                    with_previous: False
                    on_press: root.manager.current = 'students'
                    app_icon: 'data/images/home5.png'

<RememberScreen>:
    id: remember_screen
    GridLayout:
        id: main_grid
        cols: 1
        rows: 3
        ActionBar: 
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'Learning English for Kids!'
                    with_previous: False
                    on_press: root.manager.current = 'students'
                    app_icon: 'data/images/home5.png'
                
""")


class StudentsScreen(Screen):
    def init_student (self, student_name):
        pass
        """
        #load student data from file
        student_file = student_name + '.pkl'
        if os.path.exists(student_file):
            f_student = open(student_file, 'rb')
            current_student = pickle.load(f_student)
        else:
            current_student = student.Student (student_name,'A1')
        current_student.add_words ( student.learn_words )

        #attach to StudentsScreen object
        self.current_student = current_student
"""
        #create student and load knowledge from file
        self.student = Student (student_name)
        #print (self.student.knowledge)
        
        #move to another screen
        sm.current = 'scenarios'
        
        
class SettingsScreen(Screen):
    pass

class DetailsScreen(Screen):
    """
Here we need to load activity object = learn + check
iterator should contain both activities

think about common screen space for all activities.



"""         
    def on_pre_enter (self):
        """
        self.card = next(sm.screens[2].iter_flashcards)
        self.play_card ( )
        """

        if sm.screens[1].scenario == 'vocabulary':
            self.lesson = lesson.Lesson (sm.screens[0].student, sm.screens[1].scenario, sm.screens[2].catalog, lesson.approach, 15)
        if sm.screens[1].scenario in ['dialogs','interactions']:
            self.lesson = lesson.Lesson (sm.screens[0].student, sm.screens[1].scenario, sm.screens[2].catalog, None, 1)
        #print ('---LESSON:\n',self.lesson) 
        #next (self.lesson)
        self.next_card (None)
        self.play_card()
    def on_pre_leave (self):
        del sm.screens[0].student
    
    def next_card (self, move):
        self.lesson.move(move)

    def press_help (self):
        if 'answer' in self.lesson.exercise.frame.__dict__:
            self.lesson.exercise.frame.answer.play()
            print ('Sound answer:', self.lesson.exercise.frame.answer)
            if not self.lesson.exercise.checked:
                sm.screens[0].student.knowledge.update (self.lesson.exercise.frame.languageitem, update_type = 'wrong')
                self.lesson.exercise.checked = True
                print ('Add wrong:', self.lesson.exercise.frame.languageitem)
        if self.lesson.exercise.activity == 'repeat':
            self.lesson.exercise.frame.text.play(0)
            
    def press_correct (self):
        if self.lesson.exercise.activity == 'answer' and not self.lesson.exercise.checked:
            sm.screens[0].student.knowledge.update (self.lesson.exercise.frame.languageitem, update_type = 'correct')
            self.lesson.exercise.checked = True
            print ('Add correct:', self.lesson.exercise.frame.languageitem)

    def press_wrong (self):
        if self.lesson.exercise.activity == 'answer' and not self.lesson.exercise.checked:
            sm.screens[0].student.knowledge.update (self.lesson.exercise.frame.languageitem, update_type = 'wrong')
            self.lesson.exercise.checked = True
            print ('Add wrong:', self.lesson.exercise.frame.languageitem)

    def play_card (self):
        sm.screens[3].ids['word_image'].source = self.lesson.exercise.visual_source
        sm.screens[3].ids['word_text'].text = self.lesson.exercise.frame.text

        if self.lesson.exercise.activity == 'repeat':
            self.ids['btn_wrong'].icon = ''
            self.ids['btn_correct'].icon = ''
        if self.lesson.exercise.activity == 'answer':
            self.ids['btn_wrong'].icon = 'data/images/wrong.png'
            self.ids['btn_correct'].icon = 'data/images/checkmark.png'
        
        self.lesson.exercise.frame.text.play(0.1)
        print ('Sound text:', self.lesson.exercise.frame.text)
        
        
        if self.lesson.exercise.activity == 'repeat':
            sm.screens[0].student.knowledge.update (self.lesson.exercise.frame.languageitem, update_type = 'appearence') 
        
    def play_next_card (self, move):
        pass
        self.next_card (move)
        #exercise = next (self.lesson)
        self.play_card()
        #print ('play_next_card', exercise)
    def sound_li (self):
        self.lesson.exercise.frame.languageitem.play(0)
        #self.card.play_sound()
    



class VocabularyScreen (Screen):
    def on_pre_enter (self):
        """
        if len(self.children[0].children) > 0:
            for i_btn in self.children[0].children:
                self.children[0].remove_widget (i_btn)"""
                
        if sm.screens[1].scenario in ['vocabulary','memory','remember']:
            topics = [['professions','data/images/professions/professions.jpg'],['feelings','data/images/feelings/feelings.jpg'],['animals','data/animals.jpg'],['vehicles','data/transport.jpg'],['clothes','data/clothes.jpg'],['food', 'data/food.jpg'],['school','data/school.jpg'],
             ['vegetables','data/vegetables.jpg'],['fruits','data/fruits.jpg'],['berries','data/berries.jpg'],['weather','data/images/weather/weather.png'],
             ['colours','data/images/colours/colours.jpg'],['hobbies','data/images/hobbies/hobbies.jpeg'],['house','data/images/house/house1.jpg'],['time','data/images/time/time.jpg']]

            
            
        if sm.screens[1].scenario == 'dialogs':
             topics = [['introduction','data/images/dialogs/introduction/introduction.png']]
        if sm.screens[1].scenario == 'interactions':
             topics = [['give personal information','data/images/dialogs/introduction/introduction.png'],['ask personal information','data/images/interaction/ask_name.jpg']]


        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        

        #self.children[0].size_hint = (1, None)
        #self.children[0].size = (Window.width, Window.height)
        #print ('Window.width, Window.height:', Window.width, Window.height)
        
        for (topic, image) in topics:
                #print ('topic, image', topic, image)
                btn = ButtonImage (source = image, size_hint_y=None, height=int(Window.height/3))
                btn.bind (on_press = partial(self.set_catalog, topic))
                #self.children[0].children[0].add_widget(btn)
                layout.add_widget(btn)
                

        self.add_widget (ScrollView(size_hint=(1, None), size=(Window.width, Window.height)))
        self.children[0].add_widget(layout)
        
            
    def on_pre_leave (self):
        """
        #print ('VocabularyScreen:on_pre_leave')
        if len(self.children[0].children) > 0:
            #print ('Number :', len(self.children[0].children), '\nchildren:' ,self.children[0].children)
            for i_btn in self.children[0].children[0].children[:]:
                #print ('btn', i_btn.source)
                self.children[0].remove_widget (i_btn)
        """
        self.remove_widget (self.children[0])
    def set_catalog (self, topic, *args, **kwargs):
        """
        #take student and select 15 random cards
        student = sm.screens[0].current_student

        #get words to learn
        m_words = student.get_words_to_learn (topic, number = 50)

        #get flash cards
        m_flashcards = learningmaterials.flashcards.get_flashcards (topic, m_words)
        self.iter_flashcards = two_way_generator (m_flashcards)
        """
        #load catalog
        catalog.load (sm.screens[1].scenario, topic, student=sm.screens[0].student)
        
        #set subcatalog tree
        self.catalog = catalog[sm.screens[1].scenario][topic]
        #print (self.catalog)
        
        #move to another screen - should be method of scenario class!
        if sm.screens[1].scenario == 'memory':
            sm.current = 'memory'
        elif sm.screens[1].scenario == 'remember':
            sm.current = 'remember'
        else:
            sm.current = 'details'

class ScenariosScreen (Screen):
    def set_scenario (self, scenario):
        self.scenario = scenario
        if scenario == 'remember111':
            sm.current = 'remember'
        else:
            sm.current = 'vocabulary'
        #sm.current = scenario

class MemoryScreen (Screen):
    def on_pre_enter (self):
        
        cols=4
        rows=3
        
        layout = GridLayout(cols=cols, rows=rows, spacing=5)
        self.game = learningmaterials.MemoryGame(cols, rows)
        self.game.load (sm.screens[2].catalog)

        
        for (li, card_type, image) in self.game:
                btn = MemoryCard (front_image = image, back_image = self.game.back_image, languageitem=li, card_type=card_type)
                layout.add_widget(btn)
                

        self.children[0].add_widget (layout)
    def on_pre_leave (self):
        self.children[0].remove_widget (self.children[0].children[0])

class RememberScreen(Screen):
    """Will be 3 frame: remember, select, result.
#1. Cards. Sound all cards with 0.5 sec interval
#2. RememberCards. After 30 sec. Select cards
#3. Result. Win/Lost. Missed cards/ wrong cards

"""
    def on_pre_enter (self):
        #comon for all frame
        self.game = learningmaterials.RememberGame()
        self.game.load (sm.screens[2].catalog)

        self.load_frame (frame=1)
        
    def on_pre_leave (self):
        self.children[0].remove_widget (self.children[0].children[0])
    def next_frame (self, *args):
        #self.children[0].remove_widget (self.children[0].children[0])
        #self.game.next_frame ()
        self.load_frame (frame=self.game.next_frame ())
    def load_frame (self, frame):
        if frame == 1:
            self._add_cards (FlashCard, self.game.remember, cols=3)
            self._add_next_btn ()
        elif frame == 2:
            self.clean_frame (frame=1)
            self._add_cards (MemoryButton, self.game, cols=5)
            self._add_next_btn ()
            self._add_counter_lbl ()
        elif frame == 3:
            self.clean_frame (frame=2)
            missed = set(self.game.remember) -  self.game.selected
            wrong =  self.game.selected - set(self.game.remember)
            if missed or wrong:
                self._add_cards (ImageLabel, [('', image) for (li, image) in missed] + [('WRONG', image) for (li, image) in wrong], cols=4, font_size = '32sp', color=[1,0,0,0.6], bold=True)
                """
                layout = GridLayout(cols=4, spacing=5)
                for (li, image) in [('', image) for (li, image) in missed] + [('WRONG', image) for (li, image) in wrong]:
                        btn = FloatLayout ()
                        btn.add_widget (Image(source=image))
                        btn.add_widget (Label(text=li, font_size = '24sp', color=[1,0,0,0.5]))
                        layout.add_widget(btn)
                self.children[0].add_widget (layout)
                """
            else:
                self._add_ok ()
                #self._add_cards (FlashCard, [(None,'data/images/greatjob.jpeg')], cols=1)
            
        self.game.play()
    def clean_frame (self, frame):
        if frame == 1 or frame == 2:
            self.children[0].remove_widget (self.children[0].children[0])
            self.children[0].remove_widget (self.children[0].children[0])
            #self.children[0].remove_widget (self.children[0].children[1])
        elif frame == 3:
            pass
    def _add_next_btn (self):
        #add next button
        layout = RelativeLayout (size_hint = (1, 0.15))
        sub_layout = AnchorLayout (anchor_x = 'right')
        sub_layout.add_widget (ButtonImage(size_hint= (0.15, 1), source = 'data/images/next.png', on_press = self.next_frame, id = 'next_btn'))
        layout.add_widget (sub_layout)

        
        self.children[0].add_widget (layout)
        self.ids['navigation'] = layout
    def _add_counter_lbl (self):
        sub_layout = AnchorLayout (anchor_x = 'center')
        label = Label(font_size = '24sp')
        sub_layout.add_widget (label)
        self.ids['navigation'].add_widget (sub_layout)
        self.game.counter = label
    def _add_cards (self, CardClass, cards_data, cols = 3, **kwargs): 
        layout = GridLayout(cols=cols, spacing=5)
        for (li, image) in cards_data:
                btn = CardClass (languageitem=li, image = image, **kwargs)
                layout.add_widget(btn)
        self.children[0].add_widget (layout)
    def _add_ok (self):
        #layout1 = GridLayout (cols=2)
        
        layout = AnchorLayout (anchor_x = 'center')
        layout.add_widget (Image(source='data/images/greatjob.jpeg'))
        #layout.add_widget (Label(text='OK!',font_size = '24sp'))

        #layout1.add_widget (layout)
        #layout1.add_widget (Image(source='data/images/greatjob.jpeg'))

        #layout = AnchorLayout (anchor_x = 'center')
        #layout.add_widget (Image(source='data/images/greatjob.jpeg'))
        #layout.add_widget (Label(text='OK!',font_size = '24sp'))
        #layout1.add_widget (layout)
        
        self.children[0].add_widget (layout)

sm = ScreenManager()
sm.add_widget(StudentsScreen(name='students'))
sm.add_widget(ScenariosScreen(name='scenarios'))
sm.add_widget(VocabularyScreen(name='vocabulary'))
sm.add_widget(DetailsScreen(name='details'))
sm.add_widget(MemoryScreen(name='memory'))
sm.add_widget(RememberScreen(name='remember'))

#print (sm.children[0].children[0].children[2].children[0].__class__)
#print (dir(sm.children[0].children[0].children[2].children[0]))


class SampleApp(App):
    def build(self):
        return sm
    def on_stop(self):
        if 'student' in sm.screens[0].__dict__:
            del(sm.screens[0].student)


if __name__ == '__main__':
    SampleApp().run()
    #runTouchApp(SampleApp())
