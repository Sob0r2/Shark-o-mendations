import copy
import unittest
from unittest.mock import patch

import pandas as pd
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from Backend.final_results import Final_Results
from Frontend.GenresScreen.genresscreen import RightCheckbox


class TestFinalResults(unittest.TestCase):

    def setUp(self):
        self.genres = ['Drama', 'Adventure', 'Fantasy', 'Crime', 'Comedy', 'Musical','Action', 'Animation', 'Sci-Fi']
        self.data = pd.read_csv('test_data.csv')
        Final_Results.act_genres = None
        self.app = MDApp()
        self.screen = Screen(name='mainscreen')
        self.screen.app = self.app

    def test_start(self):
        self.assertIsNone(Final_Results.result)
        self.assertIsNone(Final_Results.genres)
        self.assertIsNone(Final_Results.act_genres)
        with patch.object(Final_Results, 'act_genres'),\
              patch.object(Final_Results,'genres'), \
              patch.object(Final_Results,'result'):
            Final_Results.start(self.data,self.genres)
            self.assertIsInstance(Final_Results.result,pd.DataFrame)
            self.assertIsNotNone(Final_Results.act_genres)
            self.assertEqual(self.genres, Final_Results.genres)

    def test_click_button_true(self):
        checkbox = RightCheckbox()
        mock_data = {'0':0,'1':0}
        checkbox.id = '1'
        with patch.object(Final_Results, 'act_genres', mock_data) as mock_data:
            Final_Results.click_button(checkbox)
            self.assertNotEqual({'0':0,'1':0},mock_data)

    def test_click_button_false(self):
        checkbox = RightCheckbox()
        mock_data = {'0':0,'1':1}
        checkbox.id = '1'
        with patch.object(Final_Results, 'act_genres', mock_data) as mock_data:
            Final_Results.click_button(checkbox)
            self.assertEqual({'0':0,'1':0},mock_data)

    def test_return_filtered(self):
        mock_data = {'Drama': 1, 'Adventure': 1, 'Fantasy': 1, 'Crime': 1, 'Comedy': 1, 'Musical': 1, 'Action': 1, 'Animation': 1, 'Sci-Fi': 1}
        test = copy.deepcopy(mock_data)
        with patch.object(Final_Results, 'result', self.data), \
              patch.object(Final_Results, 'org', self.data), \
              patch.object(Final_Results, 'act_genres', mock_data):
            self.assertEqual(test.items(),Final_Results.act_genres.items())
            self.assertEqual(len(Final_Results.result),5)
            self.assertEqual(Final_Results.result.at[0,'title'], 'Hidden Figures')
            Final_Results.act_genres['Drama'] = 0
            Final_Results.act_genres['Adventure'] = 0
            Final_Results.act_genres['Fantasy'] = 0
            Final_Results.return_filtered()
            self.assertNotEqual(test.items(), Final_Results.act_genres.items())
            self.assertEqual(len(Final_Results.result), 3)
            self.assertEqual(Final_Results.result.at[Final_Results.result.index[0], 'title'], 'The Night Of')

    def test_on_entry(self):
        mock_data = {'Drama': 1, 'Adventure': 1, 'Fantasy': 1}
        with patch.object(Final_Results,'act_genres', mock_data), \
              patch.object(Final_Results, 'tmp_genres', {}):
            self.assertNotEqual(Final_Results.act_genres, Final_Results.tmp_genres)
            Final_Results.on_entry()
            self.assertEqual(Final_Results.act_genres, Final_Results.tmp_genres)

    def test_delete_changes(self):
        mock_data = {'Drama': 1, 'Adventure': 1, 'Fantasy': 1}
        with patch.object(Final_Results,'act_genres', {}), \
              patch.object(Final_Results, 'tmp_genres', mock_data):
            self.assertNotEqual(Final_Results.act_genres, Final_Results.tmp_genres)
            Final_Results.on_entry()
            self.assertEqual(Final_Results.act_genres, Final_Results.tmp_genres)

    def test_check_empty(self):
        mock_data = {'Drama': 1, 'Adventure': 1}
        with patch.object(Final_Results, 'act_genres',mock_data):
            self.assertFalse(Final_Results.check_empty())
            mock_data['Drama'], mock_data['Adventure'] = 0,0
            self.assertTrue(Final_Results.check_empty())

    def test_return_vals(self):
        data_copy = copy.deepcopy(self.data)
        with patch.object(Final_Results, 'result', self.data):
            title,image_path,rating = Final_Results.return_vals(0)
            self.assertEqual(title,data_copy.at[0,'title'])
            self.assertEqual(image_path,rf"C:\Users\jakub\Projekt\photos\{data_copy.at[0, 'movieID']}.jpg",)
            self.assertEqual(rating, data_copy.at[0, 'rating'])