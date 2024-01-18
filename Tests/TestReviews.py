import json
import unittest
from unittest.mock import patch

from Backend.reviews import Reviews


class TestReviews(unittest.TestCase):

    def setUp(self):
        self.reviews = Reviews()

    def test_make_empty(self):
        # Test, czy make_empty poprawnie ustawia dane na pusty słownik
        mock_data = {'0': 1, '1': 2, '2': 5, '3': 0}
        with patch.object(self.reviews, 'data', mock_data):
            self.reviews.make_empty()
            self.assertEqual(self.reviews.data, {'0':0,'1':0,'2':0,'3':0})

    def test_watched_empty_data(self):
        # Test, czy watched zwraca False, gdy nie ma żadnych ocen
        mock_data = {'0':0,'1':0,'2':0,'3':0}
        with patch.object(self.reviews, 'data', mock_data):
            self.assertFalse(self.reviews.watched())

    def test_watched_with_data(self):
        # Test, czy watched zwraca True, gdy są jakieś oceny
        mock_data = {'0': 0, '1': 5, '2': 0, '3': 1}
        with patch.object(self.reviews, 'data', mock_data):
            self.assertTrue(self.reviews.watched())

    def test_save_method(self):
        # Test, czy save poprawnie zapisuje dane do pliku JSON
        mock_data = {'0': 3, '1': 4, '2': 5}
        with patch.object(self.reviews, 'data', mock_data):
            self.reviews.save()
            with open(r'C:\Users\jakub\Projekt\Reviews.json') as json_file:
                open_data = json.load(json_file)
                json_file.close()
            self.assertEqual(open_data, mock_data)

    def test_make_empty_calls_save(self):
        # Test, czy po wywołaniu make_empty pusty plik zapisze sie do json
        mock_data = {'0': 1, '1': 2, '2': 5, '3': 0}
        with patch.object(self.reviews, 'data', mock_data), \
                patch.object(self.reviews, 'save') as mock_save:
            self.reviews.make_empty()
            self.assertEqual(self.reviews.data, {'0': 0, '1': 0, '2': 0, '3': 0})
            mock_save.assert_called_once()
            with open(r'C:\Users\jakub\Projekt\Reviews.json') as json_file:
                open_data = json.load(json_file)
                json_file.close()
            self.assertEqual(open_data, {'0': 0, '1': 0, '2': 0, '3': 0})
