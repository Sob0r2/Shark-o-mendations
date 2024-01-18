import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
import torch

from Backend.model import Model, SAE


class TestModel(unittest.TestCase):

    @patch('torch.load')
    def setUp(self, mock_torch_load):
        mock_torch_load.return_value = MagicMock()
        self.model = Model()

    def test_get_results(self):
        with patch.object(self.model, 'ae', SAE()):
            result, genres = self.model.get_results()
            self.assertIsInstance(result, pd.DataFrame)
            expected_columns = ['title', 'genres', 'data', 'movieID', 'rating']
            self.assertListEqual(list(result.columns), expected_columns)
            self.assertGreater(len(genres), 0)
 
    def test_give_arr(self):
        input_row = "['Action', 'Adventure', 'Sci-Fi']"
        expected_output = ['Action', 'Adventure', 'Sci-Fi']
        output = self.model.give_arr(input_row)
        self.assertListEqual(output, expected_output)

    def test_get_genres(self):
        fake_output = torch.rand(995)
        fake_user_ind = [1, 2, 3]
        result = self.model.create_dataframe(fake_output, fake_user_ind)
        with patch.object(self.model, 'res', result):
            genres = self.model.get_genres()
            self.assertGreater(len(genres), 0)
            self.assertTrue('Action' in genres)

    def test_create_dataframe(self):
        fake_output = torch.rand(995)
        fake_user_ind = [1, 2, 3]
        result = self.model.create_dataframe(fake_output, fake_user_ind)
        self.assertIsInstance(result, pd.DataFrame)
        expected_columns = ['title', 'genres', 'data', 'movieID', 'rating']
        self.assertListEqual(list(result.columns), expected_columns)

    def test_to_dataframe(self):
        fake_dict = {1: 4.5, 2: 3.0, 3: 5.0}
        result = self.model.to_dataframe(fake_dict)
        self.assertIsInstance(result, pd.DataFrame)
        expected_columns = ['movieID', 'rating']
        self.assertListEqual(list(result.columns), expected_columns)
