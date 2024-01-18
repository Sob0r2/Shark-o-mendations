import json
import unittest
from unittest.mock import patch

import pandas as pd

from Backend.reviews import Reviews
from Backend.user_ratings import User_Ratings


class TestUserRatings(unittest.TestCase):

    def setUp(self):
        self.user_ratings = User_Ratings(10)

    def test_create_swipe_blocks(self):
        with patch.object(self.user_ratings, 'movies', pd.read_csv('test.csv')),\
              patch.object(self.user_ratings, 'num_of_movies', 5), \
              patch.object(self.user_ratings, 'choices', []):
            self.assertEqual(len(self.user_ratings.choices),0)
            self.user_ratings.create_swipe_blocks()
            self.assertEqual(len(self.user_ratings.choices),5)

    def test_title_and_photo_generator_if_true(self):
        with patch.object(self.user_ratings, 'movies', pd.read_csv('test.csv')), \
              patch.object(self.user_ratings, 'num_of_movies', 5), \
              patch.object(self.user_ratings, 'choices', [0,1,10,3,4]), \
              patch.object(self.user_ratings, 'act', 2):
            self.assertEqual(self.user_ratings.act,2)
            title,photo = self.user_ratings.title_and_photo_generator()
            self.assertEqual(title,'Ace Ventura: When Nature Calls')
            self.assertEqual(photo,r'C:\Users\jakub\Projekt\photos\10.jpg')
            self.assertEqual(self.user_ratings.act,3)

    def test_title_and_photo_generator_unless_true(self):
        with patch.object(self.user_ratings, 'movies', pd.read_csv('test.csv')), \
              patch.object(self.user_ratings, 'num_of_movies', 5), \
              patch.object(self.user_ratings, 'choices', [0, 1, 10, 3, 4]), \
              patch.object(self.user_ratings, 'act', 6):
            self.assertEqual(self.user_ratings.act,6)
            title, photo = self.user_ratings.title_and_photo_generator()
            self.assertEqual(title,-1)
            self.assertEqual(photo,'')
            self.assertEqual(self.user_ratings.act, 6)

    def test_rate(self):
        with patch.object(self.user_ratings, 'reviews', Reviews()), \
              patch.object(self.user_ratings.reviews, 'data', {'0':1,'1':3}) as mock_data, \
              patch.object(self.user_ratings, 'choices', [0,4,1,10,15]) as mock_choices, \
              patch.object(self.user_ratings, 'act', 3) as mock_act:
            self.assertEqual(mock_data[f'{mock_choices[mock_act-1]}'],3)
            self.user_ratings.rate(5)
            self.assertEqual(mock_data[f'{mock_choices[mock_act-1]}'],5)

    def test_to_go(self):
        with patch.object(self.user_ratings, 'act', 3), \
              patch.object(self.user_ratings, 'num_of_movies', 5):
            self.assertEqual(self.user_ratings.to_go(),'3/5')

    def test_finish_rating(self):
        open_data = {'0':0,'1':2,'2':0,'3':4}
        with open(r'C:\Users\jakub\Projekt\Reviews.json', 'w') as json_file:
            json.dump(open_data, json_file)

        with patch.object(self.user_ratings, 'reviews', Reviews), \
             patch.object(self.user_ratings.reviews, 'data', {'0': 1, '1': 2, '2': 5}) as mock_data:
            self.assertNotEqual(mock_data, open_data)
            Reviews.save(self.user_ratings.reviews)

            with open(r'C:\Users\jakub\Projekt\Reviews.json') as json_file:
                open_data = json.load(json_file)
                json_file.close()
            self.assertEqual(open_data, mock_data)
