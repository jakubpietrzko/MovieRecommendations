from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from SelectScreen import SelectScreen
from RecommendScreen import RecommendScreen
        
        
        
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SelectScreen(name='select'))
        sm.add_widget(RecommendScreen(name='recommend'))
        return sm

if __name__ == '__main__':
    MyApp().run()

