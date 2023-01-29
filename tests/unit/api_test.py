import unittest
from spotrend.api import Spotrend
from spotrend.exceptions import *


def correct_status(data : dict):
    keys = data.keys()
    return "error" not in keys


class SpotrendTest(unittest.TestCase):

    def setUp(self):
        self.st = Spotrend()

    def test_get_album(self):
        album_id = "4aawyAB9vmqN3uQ7FjRGTy"
        album = self.st.get_album(album_id)
        self.assertIsInstance(album, dict)
        
        # test response status
        keys = album.keys()
        self.assertNotIn("error", keys)

        # call API with specific market
        market = "US"
        album = self.st.get_album(album_id, market=market)
        self.assertIsInstance(album, dict)

        # define again if the status code is 2xx
        self.assertTrue(correct_status(album))


    def test_get_artist(self):
        artist_id = "0TnOYISbd1XYRBk9myaseg"
        artist = self.st.get_artist(artist_id)
        self.assertIsInstance(artist, dict)
        
        # test response status
        self.assertTrue(correct_status(artist))

    def test_get_track(self):
        track_id = "11dFghVXANMlKmJXsNCbNl"
        track = self.st.get_track(track_id)
        self.assertIsInstance(track, dict)

        # test response status
        self.assertTrue(correct_status(track))

        # call API with specific market
        market = "US"
        track = self.st.get_track(track_id, market=market)
        self.assertIsInstance(track, dict)

        # define again if the status code is 2xx
        self.assertTrue(correct_status(track))
        

    def test_available_markets(self):
        markets = self.st.get_available_markets()
        self.assertIsInstance(markets, dict)

        # test response status
        if "markets" in markets.keys():
            n = len(markets['markets'])
            self.assertGreaterEqual(n, 1)
        
        self.assertTrue(correct_status(markets))

    def test_available_genres(self):
        data = self.st.get_available_genres()
        self.assertIsInstance(data, dict)

        # test response status
        if "genres" in data.keys():
            n = len(data['genres'])
            self.assertGreater(n, 1)

        self.assertTrue(correct_status(data))

