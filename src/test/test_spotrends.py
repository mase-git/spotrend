import unittest
from main.spotrends import Spotrends

class SpotrendsTest(unittest.TestCase):

    def setUp(self):
        self.st = Spotrends() 
    
    def test_IsInstance(self):
        self.assertIsInstance(self.st, Spotrends)
    
    