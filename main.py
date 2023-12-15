from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from Frontend.FinalScreen.finalscreen import FinalScreen
from Frontend.GenresScreen.genresscreen import GenresScreen
from Frontend.LoadingScreen.loadingscreen import LoadingScreen
from Frontend.MainScreen.mainscreen import MainScreen
from Frontend.NumOfSwipesScreen.numofswipesscreen import NumOfSwipesScreen
from Frontend.SwipeScreen.swipescreen import SwipeScreen

Builder.load_file("main.kv")
Builder.load_file("Frontend/MainScreen/mainscreen.kv")
Builder.load_file("Frontend/NumOfSwipesScreen/numofswipesscreen.kv")
Builder.load_file("Frontend/SwipeScreen/swipescreen.kv")
Builder.load_file("Frontend/LoadingScreen/loadingscreen.kv")
Builder.load_file("Frontend/FinalScreen/finalscreen.kv")
Builder.load_file("Frontend/GenresScreen/genresscreen.kv")

class MainApp(MDApp):

    def build(self):
        self.title = "Shark-o-mendations"
        Window.size = (600,800)
        LabelBase.register(name='TITLE_FONT',
                           fn_regular='Graphics/Asutenan!.ttf')
        LabelBase.register(name='BUTTON_FONT',
                           fn_regular='Graphics/Healing Sunday.ttf')

        sm = MDScreenManager()

        sm.add_widget(MainScreen("mainscreen"))
        sm.add_widget(NumOfSwipesScreen("numofswipesscreen"))
        sm.add_widget(SwipeScreen("swipescreen"))
        sm.add_widget(LoadingScreen("loadingscreen"))
        sm.add_widget(FinalScreen("finalscreen"))
        sm.add_widget(GenresScreen("genresscreen"))

        sm.current = "mainscreen"
        return sm

MainApp().run()