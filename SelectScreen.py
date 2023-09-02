from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import sqlite3
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from collections import Counter

  
class MyTextInput(TextInput):
    def __init__(self,view, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.bind(text=self.on_text)
        self.dropdown = DropDown()
        self.del_after=False
        self.view=view
        self.on_select=self.view.on_select
        self.dropdown.bind(on_select=self.on_select)
        
    def on_text(self, instance, value):
          if len(value) >= 3:
            conn = sqlite3.connect('movies.db')
            c = conn.cursor()
            c.execute('SELECT title FROM movies WHERE title LIKE ?', ('%' + value + '%',))
            data = c.fetchall()
            conn.close()
            if self.dropdown.parent:
                self.dropdown.parent.remove_widget(self.dropdown)
                self.dropdown = DropDown()
                self.dropdown.bind(on_select=self.on_select)
            self.dropdown.clear_widgets()
            for row in data:
                btn = Button(text=row[0], size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(btn)
            
            self.dropdown.open(self)
           
        

class SelectScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Choose maximum 8 videos'))
        self.input = MyTextInput(multiline=False, view=self)
        layout.add_widget(self.input)
        button = Button(text='Dalej')
        button.bind(on_press=self.next_screen)
        layout.add_widget(button)
        self.add_widget(layout)

        self.selected_movies = []
        for i in range(8):
            label = Label(text='')
            layout.add_widget(label)
            self.selected_movies.append(label)

        self.input.dropdown.bind(on_select=self.on_select)
        

    def on_select(self,instance, value):
        
        for label in self.selected_movies:
            if not label.text:
                label.text = value
                break
        self.input.del_after=True
        self.input.text=''
        

    def next_screen(self, instance):
        movies = [label.text for label in self.selected_movies if label.text]
        if len(movies) == 0:
            return
        self.manager.transition.direction = 'left'
        self.manager.current = 'recommend'
        self.manager.get_screen('recommend').recommend(movies)

              