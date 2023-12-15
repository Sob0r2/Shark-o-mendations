from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from Backend.request_api import RequestApi as api
from Backend.user_ratings import User_Ratings
from Text import Text

shark = Text.shark()
star_shark = Text.star_shark()
rate_to_img = {0: [shark] * 5, 1: [star_shark] + [shark] * 4, 2: 2*[star_shark] + [shark] * 3, 3: 3*[star_shark] + [shark]*2,
               4: 4*[star_shark] + [shark], 5: 5*[star_shark]}
class SwipeScreen(MDScreen):

    ur = None
    current_title = ""
    current_image = ""
    to_go = ""
    num_of_sharks = 0


    def beginSwipe(self,val):
        self.ur = User_Ratings(val)
        self.ur.create_swipe_blocks()
        self.flag = False
        self.get_movie()

    def get_movie(self):
        title,image = self.ur.title_and_photo_generator()
        self.to_go = self.ur.to_go()
        if title == -1:
            self.ur.finish_ratings()
            self.parent.current = "loadingscreen"
        else:
            self.current_title,self.current_image = title,image
            self.ids.movie_image.source = self.current_image
            self.ids.movie_title.text = self.current_title
            self.ids.to_go.text = self.to_go

    def stars(self, star):
        self.num_of_sharks = star
        o,t,th,f,fi = rate_to_img[star]
        self.ids.one_star.source = o
        self.ids.two_star.source = t
        self.ids.three_star.source = th
        self.ids.four_star.source = f
        self.ids.five_star.source = fi

    def confirm(self):
        if self.num_of_sharks != 0:
            self.ur.rate(self.num_of_sharks)
            self.get_movie()
            self.stars(0)

    def skip(self):
        self.get_movie()
        self.stars(0)

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

    def click_text(self):
        self.show_dialog(self.current_title)

    def on_enter(self):
        Window.bind(on_keyboard=self.on_key_down)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_key_down)

    def on_key_down(self, window, key, *largs):
        if key == 27:
            self.ur.finish_ratings()
            self.parent.current = "mainscreen"
