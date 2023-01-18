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
    
    def test_track_info_by_id(self):
        pass

    def test_track_info_by_name(self):
        pass


    def test_tracks_by_artist_id(self):
        pass


    def test_tracks_by_artist_name(self):
        pass


    def test_tracks_by_ids(self):
        pass


    def test_artists_by_ids(self):
        pass


    def test_tracks_by_names(self):
        pass
    

    def test_artists_by_names(self):
        pass

    def test_album_info_by_id(self):
        pass


    def test_album_info_by_name(self):
        pass


    def test_albums_by_artist_id(self):
        pass


    def test_albums_by_artist_name(self):
        pass


    def test_album_by_ids(self):
        pass

    def test_available_markets(self):
        pass


    def test_images_by_artists_id(self):
        pass

    def test_images_by_artists_names(self):
        pass


    def test_features_by_track_id(self):
        pass


    def test_features_by_track_name(self):
        pass

    def test_features_by_tracks_ids(self):
        pass


    def test_artist_id_by_name(self):
        pass
    

    def test_artist_name_by_id(self):
        pass


    def test_track_id_by_name(self):
        pass
    

    def test_album_name_by_id(self):
        pass
            
