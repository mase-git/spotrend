import unittest
from src.main.spotrends import Spotrends

class SpotrendsTest(unittest.TestCase):

    def setUp(self):
        self.st = Spotrends() 
    
    def isInstance(self):
        self.assertIsInstance(self.st, Spotrends)
