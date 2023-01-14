import unittest
from unittest.mock import patch
from spotrends.client import Spotrends
from spotrends.exceptions import SpotrendsInputException

def return_expected_a_vals():
    return [str, int, list, str, str, str, int, str, str]

def return_expected_a_key():
    return ['spotify_url', 'followers', 'genres', 'id', 'image', 'name', 'popularity', 'type', 'uri']

class SpotrendsTest(unittest.TestCase):

    def setUp(self):
        self.st = Spotrends(0, 1)
        self._expected_a_key = return_expected_a_key()
        self._expected_a_vals = return_expected_a_vals()

    def test_isIstance(self):
        self.assertIsInstance(self.st, Spotrends)

    def test_artist_info_by_id(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.artist_info_by_id('no-valid-id')
        out = self.st.artist_info_by_id('2WX2uTcsvV5OnS0inACecP')
        self.assertIsInstance(out, dict)
        self.assertListEqual(list(out.keys()), self._expected_a_key)
        self.assertListEqual(list(map(type, list(out.values()))), self._expected_a_vals)

    def test_artist_info_by_name(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.artist_info_by_name('wrong_name')
        out = self.st.artist_info_by_name('Drake')
        self.assertIsInstance(out, dict)
        
            
