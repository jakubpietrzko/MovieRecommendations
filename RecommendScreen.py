from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import sqlite3
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
import pandas as pd
import numpy as np
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from collections import Counter
from tensorflow.keras.models import load_model
  
class RecommendScreen(Screen):
    def __init__(self, **kwargs):
        super(RecommendScreen, self).__init__(**kwargs)
        self.ff={}
        self.batch_size=200
        self.maxim=1
        self.the_bests=1
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Recommends::", size_hint_y=1)
        self.layout.add_widget(self.label)
        self.movies_lab = []
        for i in range(8):
            label = Label(text='')
            self.layout.add_widget(label)
            self.movies_lab.append(label)
        """self.grid_layout = GridLayout(cols=2, size_hint_y=10, pos_hint={'top': 1})
        self.layout.add_widget(self.grid_layout)"""
        self.button1 = Button(text='More')
        self.button1.bind(on_press=self.more)
        self.layout.add_widget(self.button1)
        self.button2 = Button(text='Try rate all (long time)')
        self.button2.bind(on_press=self.all)
        self.layout.add_widget(self.button2)
        self.add_widget(self.layout)
    def more(self, instance):
        film_data = self.search_movie()
        i=0
        for label in self.movies_lab:        
            label.text = str(film_data.iloc[i]['title'])+ "     "+str(film_data.iloc[i]['rating'])
            i+=1
        
    def all(self,instance):
        model1=load_model("recommendation_model2.h5")
        
        columns_50 = [f'PCA{i}' for i in range(1, 51)]
        col_str50 = ', '.join(columns_50)
        conn = sqlite3.connect('movies.db')
        counter=0
        
        query = f'SELECT {col_str50} FROM movies'
        counter+=1            
        batch_df = pd.read_sql(query, conn)
        v=0
        for i in batch_df.index:
                v+=1
                input2pr = np.array(batch_df.loc[[i]]).reshape(1, -1)
                pred = model1.predict([self.input1pr,input2pr])
                print(i)
                print("bestie",self.the_bests, self.maxim)
                if pred>self.min_to_be_accept:
                    self.ff[i]=pred
                if pred>self.maxim:
                    self.the_bests=i
                    self.maxim=pred
                """if v%10==1 and v>batch_size//2 and len(ff)<=3:
                    min_to_be_accept-=0.1
                     if counter >8:
                self.min_to_be_accept-=0.1
                if len(self.ff)>=8 or counter>12:
                x=False
                if len(self.ff)==0:
                    self.ff[self.the_bests]=self.maxim"""
        ff_keys = list(self.ff.keys())

        ffstr = str(ff_keys).replace('[', '(').replace(']', ')')

        film_data=pd.read_sql(f'SELECT title, movieId FROM movies WHERE movieId IN {ffstr}',conn)
             
        conn.close()
        film_data['rating'] = film_data['movieId'].map(self.ff)
        """self.grid_layout.clear_widgets()
        self.grid_layout.add_widget(Label(text="Tytuł"))
        self.grid_layout.add_widget(Label(text="Ocena"))
        for idx, row in film_data.iterrows():
            self.grid_layout.add_widget(Label(text=row['title']))
            self.grid_layout.add_widget(Label(text=str(row['rating'])))
        """
        film_data = film_data.sort_values(by='rating', ascending=False)
        
        print(film_data.head(8))
       
        
        i=0
        for label in self.movies_lab:        
            label.text = str(film_data.iloc[i]['title'])+ "     "+str(film_data.iloc[i]['rating'])
            i+=1
    def search_movie(self):
        model1=load_model("recommendation_model1.h5")
        x=True
        columns_50 = [f'PCA{i}' for i in range(1, 51)]
        col_str50 = ', '.join(columns_50)
        conn = sqlite3.connect('movies.db')
        
        
        query = f'SELECT movieId,{col_str50} FROM movies ORDER BY RANDOM() LIMIT {self.batch_size} '
                
        batch_df = pd.read_sql(query, conn)
        movie_ids = batch_df['movieId']
        
        v=0
        for i in movie_ids:
                v+=1
                input2pr = np.array(batch_df[batch_df['movieId']==i]).reshape(1, -1)
                input2pr=input2pr[:,1:] 
                pred = model1.predict([self.input1pr,input2pr])
                print(i)
                print("bestie",self.the_bests, self.maxim)
                if pred>self.min_to_be_accept:
                    self.ff[i]=pred
                if pred>self.maxim:
                    self.the_bests=i
                    self.maxim=pred
                """if v%10==1 and v>batch_size//2 and len(ff)<=3:
                    min_to_be_accept-=0.1
                     if counter >8:
                self.min_to_be_accept-=0.1
                if len(self.ff)>=8 or counter>12:
                x=False
                if len(self.ff)==0:
                    self.ff[self.the_bests]=self.maxim"""
        ff_keys = list(self.ff.keys())

        ffstr = str(ff_keys).replace('[', '(').replace(']', ')')

        film_data=pd.read_sql(f'SELECT title, movieId FROM movies WHERE movieId IN {ffstr}',conn)
             
        conn.close()
        film_data['rating'] = film_data['movieId'].map(self.ff)
        """self.grid_layout.clear_widgets()
        self.grid_layout.add_widget(Label(text="Tytuł"))
        self.grid_layout.add_widget(Label(text="Ocena"))
        for idx, row in film_data.iterrows():
            self.grid_layout.add_widget(Label(text=row['title']))
            self.grid_layout.add_widget(Label(text=str(row['rating'])))
        """
        film_data = film_data.sort_values(by='rating', ascending=False)
        
        print(film_data.head(8))
        print(batch_df.head(15))
        return film_data
        
    def recommend(self, movies):
        
        conn = sqlite3.connect('movies.db')
        
        movies_str = str(movies).replace('[', '(').replace(']', ')')
       
        
        columns = [f'PCA{i}' for i in range(1, 21)]
        columns_str = ', '.join(columns)
        
        
        user_data = pd.read_sql(f'SELECT {columns_str} FROM movies WHERE title in {movies_str}', conn)
        i = 0
        while user_data.shape[0] < 8:
            user_data = user_data._append(user_data.iloc[i], ignore_index=True)
            i += 1

        user_data=user_data.stack().reset_index(drop=True)
        self.input1pr = np.array(user_data).reshape(1, -1)
        conn.close()
        
        self.min_to_be_accept=3.0
        
        film_data = self.search_movie()
        i=0
        for label in self.movies_lab:        
                if i<8:
                    label.text = str(film_data.iloc[i]['title'])+ "     "+str(film_data.iloc[i]['rating'])
                    i+=1
    