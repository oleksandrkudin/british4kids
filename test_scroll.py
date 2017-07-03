from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from functools import partial

"""
layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
# Make sure the height is such that there is something to scroll.
layout.bind(minimum_height=layout.setter('height'))
for i in range(100):
    btn = Button(text=str(i), size_hint_y=None, height=40)
    layout.add_widget(btn)
root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
root.add_widget(layout)
"""


class ButtonImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ButtonImage, self).__init__(**kwargs)

topics = [['animals','data/animals.jpg'],['vehicles','data/transport.jpg'],['clothes','data/clothes.jpg'],['food', 'data/food.jpg'],['school','data/school.jpg'],
             ['vegetables','data/vegetables.jpg'],['fruits','data/fruits.jpg'],['berries','data/berries.jpg'],['weather','data/images/weather/weather.png'],
             ['colours','data/images/colours/colours.jpg'],['hobbies','data/images/hobbies/hobbies.jpeg']]

            
            



layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
layout.bind(minimum_height=layout.setter('height'))        

        #self.children[0].size_hint = (1, None)
        #self.children[0].size = (Window.width, Window.height)
        #print ('Window.width, Window.height:', Window.width, Window.height)
        
for (topic, image) in topics:
                #print ('topic, image', topic, image)
                btn = ButtonImage (source = image, size_hint_y=None, height=int(Window.height/3))
                #btn.bind (on_press = partial(self.set_catalog, topic))
                #self.children[0].children[0].add_widget(btn)
                layout.add_widget(btn)
                

root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
root.add_widget(layout)

runTouchApp(root)
