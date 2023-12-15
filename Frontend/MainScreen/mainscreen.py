from kivy.config import Config
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from Backend.reviews import Reviews
from Text import Text

Config.set('kivy', 'exit_on_escape', '0')

class MainScreen(MDScreen):

    reviews = None
    def show_dialog(self):
        self.dialog = MDDialog(
            title=Text.restore_text(),
            md_bg_color=(0.8, 0.8, 0.8, 1),
            buttons=[
                MDFlatButton(
                    text="YES",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_size=30,
                    font_name="TITLE_FONT",
                    on_release=lambda *args: self.close_dialog(1),
                ),
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_size=30,
                    font_name="TITLE_FONT",
                    on_release=lambda *args: self.close_dialog(0),
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, flag):
        if flag:
            self.reviews.make_empty()
        self.dialog.dismiss()

    def on_click(self):
        if self.reviews.watched():
            self.show_dialog()
        self.manager.current = "numofswipesscreen"

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_key_down)

    def on_enter(self):
        self.reviews = Reviews()
        Window.bind(on_keyboard=self.on_key_down)

    def on_key_down(self, window, key, *largs):
        if key == 27:
            app = MDApp()
            app.stop()

    def exit(self):
        app = MDApp()
        app.stop()