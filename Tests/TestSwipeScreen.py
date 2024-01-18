import unittest
from unittest.mock import patch, MagicMock

from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from Backend.user_ratings import User_Ratings
from Frontend.SwipeScreen.swipescreen import SwipeScreen


class TestSwipeScreen(unittest.TestCase):

    def setUp(self):
        self.app = MDApp()
        self.screen = SwipeScreen(name='swipescreen')
        self.screen.app = self.app
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(self.screen)
        self.loadingscreen = Screen(name='loadingscreen')
        self.mainscreen = Screen(name='mainscreen')
        self.manager.add_widget(self.loadingscreen)
        self.manager.add_widget(self.mainscreen)
        LabelBase.register(name='TITLE_FONT',
                           fn_regular=r'C:\Users\jakub\Projekt\Graphics\Asutenan!.ttf')
        LabelBase.register(name='BUTTON_FONT',
                           fn_regular=r'C:\Users\jakub\Projekt\Graphics\Healing Sunday.ttf')

    def test_beginSwipe(self):
        self.assertIsNone(self.screen.ur)
        self.assertIsNone(self.screen.flag)
        mock_create_swipe_blocks = MagicMock()
        with patch.object(self.screen, 'get_movie', return_value=True), \
              patch.object(self.screen, 'ur', User_Ratings),\
              patch.object(self.screen.ur, 'create_swipe_blocks', mock_create_swipe_blocks):
            self.screen.beginSwipe(25)
            self.assertIsNotNone(self.screen.ur)
            mock_create_swipe_blocks.assert_called_once()
            self.assertIsNotNone(self.screen.flag)

    def test_get_movie_not_title(self):
        mock_data = (-1, '')
        with patch.object(self.screen, 'ur', User_Ratings), \
              patch.object(self.screen.ur, 'title_and_photo_generator', return_value=mock_data), \
              patch.object(self.screen.ur, 'to_go', return_value=1), \
              patch.object(self.screen.ur, 'finish_ratings', return_value=True):
            self.assertEqual(self.manager.current, 'swipescreen')
            self.screen.get_movie()
            self.screen.ur.finish_ratings.assert_called_once()
            self.assertEqual(self.manager.current, 'loadingscreen')

    def test_get_movie_with_title(self):
        mock_data = ('Toy Story', r'C:\Users\jakub\Projekt\photos\0.jpg')
        mock_to_go = '10'

        self.screen.ur = User_Ratings(100)
        self.screen.ur.title_and_photo_generator = MagicMock(return_value=mock_data)
        self.screen.ur.to_go = MagicMock(return_value=mock_to_go)

        self.screen.ids = {
            'movie_title': MDLabel(text=''),
            'movie_image': Image(source=''),
            'to_go': MDLabel(text=''),
        }

        self.assertNotEqual(self.screen.ids['movie_title'].text, mock_data[0])
        self.assertNotEqual(self.screen.ids['movie_image'].source, mock_data[1])
        self.assertNotEqual(self.screen.ids['to_go'].text, mock_to_go)

        self.screen.get_movie()

        self.assertEqual(self.screen.ids['movie_title'].text, mock_data[0])
        self.assertEqual(self.screen.ids['movie_image'].source, mock_data[1])
        self.assertEqual(self.screen.ids['to_go'].text, mock_to_go)

    def test_stars(self):
        self.assertEqual(self.screen.num_of_sharks, 0)
        self.screen.ids = {
            'one_star': Image(source=self.screen.shark),
            'two_star': Image(source=self.screen.shark),
            'three_star': Image(source=self.screen.shark),
            'four_star': Image(source=self.screen.shark),
            'five_star': Image(source=self.screen.shark),
        }
        self.screen.stars(4)
        self.assertEqual(self.screen.num_of_sharks, 4)
        self.assertEqual(self.screen.ids['one_star'].source, self.screen.star_shark)
        self.assertEqual(self.screen.ids['two_star'].source, self.screen.star_shark)
        self.assertEqual(self.screen.ids['three_star'].source, self.screen.star_shark)
        self.assertEqual(self.screen.ids['four_star'].source, self.screen.star_shark)
        self.assertEqual(self.screen.ids['five_star'].source, self.screen.shark)

    def test_confirm(self):
        with patch.object(self.screen, 'num_of_sharks', 3), \
              patch.object(self.screen, 'ur', User_Ratings), \
              patch.object(self.screen.ur, 'rate'), \
              patch.object(self.screen, 'get_movie'), \
              patch.object(self.screen, 'stars'):
            self.screen.ur.rate.assert_not_called()
            self.screen.get_movie.assert_not_called()
            self.screen.stars.assert_not_called()
            self.screen.confirm()
            self.screen.ur.rate.assert_called_once()
            self.screen.get_movie.assert_called_once()
            self.screen.stars.assert_called_once()

    def test_confirm_zero(self):
        with patch.object(self.screen, 'num_of_sharks', 0), \
                patch.object(self.screen, 'ur', User_Ratings), \
                patch.object(self.screen.ur, 'rate'), \
                patch.object(self.screen, 'get_movie'), \
                patch.object(self.screen, 'stars'):
            self.screen.confirm()
            self.screen.ur.rate.assert_not_called()
            self.screen.get_movie.assert_not_called()
            self.screen.stars.assert_not_called()

    def test_show_dialog(self):
        test_text = "Toy Story"
        self.assertIsNone(self.screen.dialog)
        self.screen.show_dialog(test_text)
        self.assertIsNotNone(self.screen.dialog)
        self.assertTrue(self.screen.dialog._window)
        self.assertEqual(self.screen.dialog.title, test_text)

    def test_close_dialog(self):
        with  patch.object(self.screen, 'dialog', MDDialog), \
                patch.object(self.screen.dialog, 'dismiss'):
            self.screen.close_dialog(None)
            self.screen.dialog.dismiss.assert_called_once()

    def test_click_text(self):
        with patch.object(self.screen, 'show_dialog'):
            self.screen.show_dialog.assert_not_called()
            self.screen.click_text()
            self.screen.show_dialog.assert_called_once()