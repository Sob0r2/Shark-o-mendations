import unittest
from unittest.mock import patch

from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

from Backend.reviews import Reviews
from Frontend.MainScreen.mainscreen import MainScreen


class TestMainScreen(unittest.TestCase):
    def setUp(self):
        self.app = MDApp()
        self.screen = MainScreen(name='mainscreen')
        self.screen.app = self.app
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(self.screen)
        self.numofswipesscreen = Screen(name="numofswipesscreen")
        self.manager.add_widget(self.numofswipesscreen)
        self.manager.current = 'mainscreen'

    def test_on_click_watched(self):
        # Sprawdzamy, czy po kliknięciu przycisku, gdy recenzje są obejrzane, wywoływana jest metoda show_dialog
        with patch.object(self.screen, 'reviews', Reviews()), \
             patch.object(self.screen.reviews, 'watched', return_value=True), \
             patch.object(self.screen, 'show_dialog') as mock_show_dialog:
            self.screen.on_click()
            mock_show_dialog.assert_called_once()
            self.assertEqual(self.manager.current,'numofswipesscreen')

    def test_on_click_not_watched(self):
        # Sprawdzamy, czy po kliknięciu przycisku, gdy recenzje nie są obejrzane, nie wywołuje się metoda show_dialog
        with patch.object(self.screen, 'reviews', Reviews), \
             patch.object(self.screen.reviews, 'watched', return_value=False), \
             patch.object(self.screen, 'show_dialog') as mock_show_dialog:
            self.screen.on_click()
            mock_show_dialog.assert_not_called()
            self.assertEqual(self.manager.current, 'numofswipesscreen')

    def test_on_enter_bind(self):
        # Sprawdzamy, czy on enter tworzy reviews
        self.manager.current = 'mainscreen'
        self.assertIsNotNone(self.screen.reviews)

    def test_exit(self):
        # Sprawdzamy, czy metoda exit kończy aplikację
        with patch.object(self.screen, 'app', MDApp), \
             patch.object(self.screen.app, 'stop') as mock_stop:
            self.screen.exit()
            mock_stop.assert_called_once()

    def test_show_dialog(self):
        # Sprawdzamy, czy metoda show_dialog tworzy i otwiera dialog
        self.assertIsNone(self.screen.dialog)
        self.screen.show_dialog()
        self.assertIsNotNone(self.screen.dialog)
        self.assertTrue(self.screen.dialog._window)

    def test_close_dialog_positive(self):
        # Sprawdzamy, czy close_dialog zmienia dane recenzji na puste po potwierdzeniu w dialogu
        with patch.object(self.screen, 'reviews', Reviews), \
             patch.object(self.screen.reviews, 'make_empty'), \
             patch.object(self.screen, 'dialog', MDDialog), \
             patch.object(self.screen.dialog, 'dismiss'):
                self.screen.show_dialog()
                self.screen.close_dialog(1)
                self.screen.reviews.make_empty.assert_called_once()
                self.screen.dialog.dismiss.assert_called_once()

    def test_close_dialog_negative(self):
        # Sprawdzamy, czy close_dialog nie zmieni danych recenzji na puste po wybraniu no w dialogu
        with patch.object(self.screen, 'reviews', Reviews), \
                patch.object(self.screen.reviews, 'make_empty'), \
                patch.object(self.screen, 'dialog', MDDialog), \
                patch.object(self.screen.dialog, 'dismiss'):
            self.screen.show_dialog()
            self.screen.close_dialog(0)
            self.screen.reviews.make_empty.assert_not_called()
            self.screen.dialog.dismiss.assert_called_once()

