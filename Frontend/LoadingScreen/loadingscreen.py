from threading import Thread

from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen

from Backend.final_results import Final_Results
from Backend.model import Model

Config.set('kivy', 'exit_on_escape', '0')

class LoadingScreen(MDScreen):

    res = None
    model_thread = None
    spinner_duration = 1
    progress_interval = 0.01

    def create_model(self, *args):
        self.model = Model()
        self.res,self.genres = self.model.get_results()
        print("finish")

    def show_final_screen(self, *args):
        if self.res is not None:
            final_res = Final_Results()
            final_res.start(self.res,self.genres)
            final_screen = self.manager.get_screen("finalscreen")
            final_screen.on_enter()
            self.manager.current = "finalscreen"
        else:
            Clock.schedule_once(self.show_final_screen, self.progress_interval)

    def update_spinner(self, dt):
        if self.ids.spinner.value < 100:
            self.ids.spinner.text = f"{self.ids.spinner.value+1}%"
            self.ids.spinner.value += 1
            Clock.schedule_once(self.update_spinner, self.progress_interval)
        else:
            Clock.schedule_once(self.show_final_screen, 0)

    def on_enter(self):
        self.ids.spinner.value = 0
        Clock.schedule_once(self.update_spinner, self.progress_interval)

        self.model_thread = Thread(target=self.create_model)
        self.model_thread.start()

        Window.bind(on_keyboard=self.on_key_down)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_key_down)

    def on_key_down(self, window, key, *largs):
        if key == 27:
            self.parent.current = "mainscreen"
            return True
