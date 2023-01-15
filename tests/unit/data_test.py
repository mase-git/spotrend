import unittest
from unittest.mock import patch
from spotrend.client import Spotrends
from spotrend.exceptions import SpotrendsInputException


class SpotrendsTest(unittest.TestCase):

    def setUp(self):
        self.st = Spotrends() # offset 0 and limit 1

    def test_isIstance(self):
        self.assertIsInstance(self.st, Spotrends)

    def test_artist_info_by_id(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.artist_info_by_id('no-valid-id')
        out = self.st.artist_info_by_id('2WX2uTcsvV5OnS0inACecP')
        self.assertIsInstance(out, dict)

    def test_artist_info_by_name(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.artist_info_by_name('wrong_name')
        out = self.st.artist_info_by_name('Drake')
        self.assertIsInstance(out, dict)
        
            
