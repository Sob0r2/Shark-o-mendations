from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineRightIconListItem, ImageRightWidget
from kivymd.uix.screen import MDScreen

from Backend.final_results import Final_Results
from Backend.request_api import RequestApi as api

Config.set('kivy', 'exit_on_escape', '0')
class FinalScreen(MDScreen):
    listcreator = None

    def on_enter(self, *args):
        self.listcreator = Final_Results()
        self.ids.list_items.clear_widgets()

        for i in range(50):
            try:
                text, image_path, rating = self.listcreator.return_vals(i)
            except (IndexError, KeyError):
                break

            image = ImageRightWidget(source=image_path,
                                     size_hint=(None, None),
                                     size=(50, 80),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})

            item = ThreeLineRightIconListItem(
                text=f"[size=30][font=Mvboli.ttf][color=#002A55][b]{text}[/font][/b][/size][/color]",
                secondary_text=f"[size=22][color={self.get_color(i)}]{rating}%[/size][/color]",
            )

            item.bind(on_release=lambda instance, text=text: self.show_dialog(text))

            item.add_widget(image)
            self.ids.list_items.add_widget(item)

    def show_dialog(self, title):
        actors,overview = api.single_movie_search(title)
        genres = api.get_genres(title)
        self.__dialog = MDDialog(
            title=f"{title}",
            text=f"Genres: {genres}\n\nActors: {actors}\n\nOverview: {overview}",
            md_bg_color="#E0E0E0",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    font_name="TITLE_FONT",
                    font_size=30,
                    on_release=self.close_dialog,
                )
            ],
        )
        self.__dialog.open()

    def close_dialog(self, *args):
        self.__dialog.dismiss()

    def get_color(self,i):
        if i <= 10: return "009900"
        elif i <= 20: return "66CC00"
        elif i <= 30: return "FFFF00"
        elif i <= 40: return "FF9933"
        else: return "FF0000"
    def exit(self):
        self.parent.current = "mainscreen"

    def filter(self):
        genres_screen = self.manager.get_screen("genresscreen")
        genres_screen.on_enter()
        self.parent.current = "genresscreen"

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_key_down)

    def on_key_down(self, window, key, *largs):
        if key == 27:
            self.parent.current = "mainscreen"
            return True