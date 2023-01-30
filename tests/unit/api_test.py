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
    
    def test_get_playlist(self):
        playlist_id = "3cEYpjA9oz9GiPac4AsH4n"
        playlist = self.st.get_playlist(playlist_id)
        self.assertIsInstance(playlist, dict)

        # test response status
        self.assertTrue(correct_status(playlist))

        # call API with specific market
        market = "US"
        playlist = self.st.get_playlist(playlist_id, market=market)
        self.assertIsInstance(playlist, dict)

        # define again the correct 2xx status code
        self.assertTrue(correct_status(playlist))

        # adding also the fields query
        fields = "items(added_by.id,track(name,href,album(name,href)))"
        playlist = self.st.get_playlist(playlist_id, fields=fields, market=market)
        self.assertIsInstance(playlist, dict)

        # define again the correct 2xx status code
        self.assertTrue(correct_status(playlist))


        # finally, adding the additional_types
        additional_type="track" # playlist of track

        playlist = self.st.get_playlist(playlist_id, additional_type=additional_type, fields=fields, market=market)
        self.assertIsInstance(playlist, dict)

        # define again the correct 2xx status code
        self.assertTrue(correct_status(playlist))

    def test_get_episode(self):
        episode_id = "512ojhOuo1ktJprKbVcKyQ"
        episode = self.st.get_episode(episode_id)
        self.assertIsInstance(episode, dict)

        # test response status
        self.assertTrue(correct_status(episode))

        # call API with specific market
        market = "US"
        episode = self.st.get_track(episode_id, market=market)
        self.assertIsInstance(episode, dict)

        # define again if the status code is 2xx
        self.assertTrue(correct_status(episode))


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

