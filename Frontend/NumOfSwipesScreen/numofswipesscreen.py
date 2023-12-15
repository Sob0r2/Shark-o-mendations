from functools import partial

from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from Text import Text

Config.set('kivy', 'exit_on_escape', '0')

from Backend.reviews import Reviews

class NumOfSwipesScreen(MDScreen):

    instruction_read = None
    def on_enter(self):
        self.reviews = Reviews()
        self.instruction_read = self.reviews.watched()
        print(self.instruction_read)
        Window.bind(on_keyboard=self.on_key_down)

    def show_dialog(self, info_text, button_text):
        self.dialog = MDDialog(
            title=info_text,
            md_bg_color=(0.8, 0.8, 0.8, 1),
            buttons=[
                MDFlatButton(
                    text=button_text,
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_size=30,
                    font_name="TITLE_FONT",
                    on_release=self.close_dialog,
                ),
            ],
        )
        self.dialog.open()

    def choose_nb_movies(self):
        self.dialog = MDDialog(
            title="Choose number of movies to rate",
            md_bg_color=(0.8, 0.8, 0.8, 1),
            buttons=[
                MDFlatButton(
                    text="25",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_size=30,
                    font_name="TITLE_FONT",
                    on_release=partial(self.close_dialog, 25),
                ),
                MDFlatButton(
                    text="50",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_size=30,
                    font_name="TITLE_FONT",
                    on_release=partial(self.close_dialog, 50),
                ),
                MDFlatButton(
                    text="100",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_size=30,
                    font_name="TITLE_FONT",
                    on_release=partial(self.close_dialog, 100),
                    halign="right"
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, value, *args):
        if isinstance(value, int):
            swipescreen = self.parent.get_screen("swipescreen")
            swipescreen.beginSwipe(value)
            self.parent.current = "swipescreen"
        self.dialog.dismiss()

    def infoButton(self):
        self.instruction_read = True
        self.show_dialog(Text.instructions(), "I understand")

    def skipButton(self):
        if self.reviews.watched():
            self.parent.current = "loadingscreen"
        else:
            self.show_dialog(Text.no_rate(), "OK")

    def processButton(self):
        if self.instruction_read or self.reviews.watched():
            self.choose_nb_movies()
        else:
            self.show_dialog(Text.first_usage(), "OK")

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_key_down)

    def on_key_down(self, window, key, *largs):
        if key == 27:
            self.parent.current = "mainscreen"

    def exit(self):
        self.parent.current = "mainscreen"
