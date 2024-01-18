import unittest
from unittest.mock import patch, Mock

from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

from Backend.reviews import Reviews
from Frontend.NumOfSwipesScreen.numofswipesscreen import NumOfSwipesScreen


class TestMainScreen(unittest.TestCase):

    def setUp(self):
        self.app = MDApp()
        self.screen = NumOfSwipesScreen(name='numofswipesscreen')
        self.screen.app = self.app
        self.manager = ScreenManager()
        self.manager.add_widget(self.screen)
        self.swipesscreen = Screen(name="swipescreen")
        self.swipesscreen.beginSwipe = Mock()
        self.loadingscreen = Screen(name='loadingscreen')
        self.mainscreen = Screen(name='mainscreen')
        self.manager.add_widget(self.swipesscreen)
        self.manager.add_widget(self.loadingscreen)
        self.manager.add_widget(self.mainscreen)
        self.manager.current = 'numofswipesscreen'
        LabelBase.register(name='TITLE_FONT',
                           fn_regular=r'C:\Users\jakub\Projekt\Graphics\Asutenan!.ttf')

    def test_on_enter(self):
        # Test, czy on_enter ustawia zmienne przy zmianie ekranu (zmiana ekranu w set_up)
        self.assertIsNotNone(self.screen.reviews)
        self.assertIsNotNone(self.screen.instruction_read)


    def test_show_dialog(self):
        # Sprawdzamy czy dialog sie otwiera i czy pokazuje odpowiedni tekst
        test_text = "text"
        test_button = "button"
        self.assertIsNone(self.screen.dialog)
        self.screen.show_dialog(test_text, test_button)
        self.assertIsNotNone(self.screen.dialog)
        self.assertTrue(self.screen.dialog._window)
        self.assertEqual(self.screen.dialog.title, test_text)
        self.assertEqual(self.screen.dialog.buttons[0].text, test_button)

    def test_choose_nb_movies_dialog(self):
        # Sprawdzamy czy dialog sie otwiera
        self.assertIsNone(self.screen.dialog)
        self.screen.choose_nb_movies()
        self.assertIsNotNone(self.screen.dialog)
        self.assertTrue(self.screen.dialog._window)

    def test_close_dialog_show_dialog(self):
        with  patch.object(self.screen, 'dialog', MDDialog), \
              patch.object(self.screen.dialog, 'dismiss'):
            self.screen.close_dialog(None)
            self.assertEqual(self.manager.current, 'numofswipesscreen')
            self.screen.dialog.dismiss.assert_called_once()

    def test_close_dialog_choose_nb(self):
        with patch.object(self.screen, 'dialog', MDDialog), \
             patch.object(self.screen.dialog, 'dismiss'):
            self.screen.close_dialog(50)
            self.assertEqual(self.manager.current, 'swipescreen')
            self.screen.dialog.dismiss.assert_called_once()

    def test_info_button(self):
        with patch.object(self.screen, 'instruction_read', False):
            self.assertIsNone(self.screen.dialog)
            self.assertFalse(self.screen.instruction_read)
            self.screen.infoButton()
            self.assertTrue(self.screen.instruction_read)
            self.assertIsNotNone(self.screen.dialog)

    def test_skip_button_if_watched(self):
        with patch.object(self.screen, 'reviews', Reviews), \
             patch.object(self.screen.reviews, 'watched', return_value=True):
            self.assertEqual(self.manager.current, 'numofswipesscreen')
            self.screen.skipButton()
            self.assertEqual(self.manager.current, 'loadingscreen')

    def test_skip_button_unless_watched(self):
        with patch.object(self.screen, 'reviews', Reviews), \
             patch.object(self.screen.reviews, 'watched', return_value=False):
            self.assertIsNone(self.screen.dialog)
            self.assertEqual(self.manager.current, 'numofswipesscreen')
            self.screen.skipButton()
            self.assertEqual(self.manager.current, 'numofswipesscreen')
            self.assertIsNotNone(self.screen.dialog)

    def test_process_button_dialog_true(self):
        with patch.object(self.screen, 'reviews', Reviews), \
              patch.object(self.screen.reviews, 'watched', return_value=True), \
              patch.object(self.screen, 'instruction_read', False):
            self.assertIsNone(self.screen.dialog)
            self.screen.processButton()
            self.assertIsNotNone(self.screen.dialog)
            self.assertEqual(self.screen.dialog.title,"Choose number of movies to rate")


    def test_process_button_dialog_false(self):
        with patch.object(self.screen, 'reviews', Reviews), \
              patch.object(self.screen.reviews, 'watched', return_value=False), \
              patch.object(self.screen, 'instruction_read', False):
            self.assertIsNone(self.screen.dialog)
            self.screen.processButton()
            self.assertIsNotNone(self.screen.dialog)
            self.assertNotEqual(self.screen.dialog.title, "Choose number of movies to rate")

    def test_exit_button(self):
        self.assertEqual(self.manager.current, 'numofswipesscreen')
        self.screen.exit()
        self.assertEqual(self.manager.current, 'mainscreen')

