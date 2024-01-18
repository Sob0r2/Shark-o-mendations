import unittest

from Backend.request_api import RequestApi


class TestRequestApi(unittest.TestCase):

    def test_get_genres(self):
        res = 'Adventure, Animation, Children,'
        self.assertEqual(RequestApi.get_genres('Toy Story'), res)

    def test_get_actors(self):
        res = 'Tom Hanks, Tim Allen, Don Rickles, Jim Varney, Wallace Shawn, John Ratzenberger, Annie Potts, John Morris, Erik von Detten, Laurie Metcalf'
        self.assertEqual(RequestApi.get_actors(862),res)

    def test_sigle_movie_search(self):
        overview = 'Led by Woody, Andy\'s toys live happily in his room until Andy\'s birthday brings Buzz Lightyear onto the scene. Afraid of losing his place in Andy\'s heart, Woody plots against Buzz. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences.'
        self.assertEqual(RequestApi.single_movie_search('Toy Story')[1], overview)