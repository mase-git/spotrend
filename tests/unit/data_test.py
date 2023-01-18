import unittest
from spotrend.client import Spotrends
from spotrend.exceptions import SpotrendsInputException


class SpotrendsTest(unittest.TestCase):

    def setUp(self):
        self.st = Spotrends() # offset 0 and limit 1
        self.valid_artist_id = "spotify:artist:2WX2uTcsvV5OnS0inACecP"
        self.valid_track_id = "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
        self.valid_album_id = "spotify:album:5MS3MvWHJ3lOZPLiMxzOU6"
        self.valid_artist_name = "Drake"
        self.valid_track_name = "Rich Flex"
        self.valid_album_name = "Her Loss" 

    def test_isIstance(self):
        self.assertIsInstance(self.st, Spotrends)

    def test_artist_info_by_id(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.artist_info_by_id('no_valid_id')
            self.st.artist_info_by_id('')
        out = self.st.artist_info_by_id(self.valid_artist_id)
        self.assertIsInstance(out, dict)

    def test_artist_info_by_name(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.artist_info_by_name('no_valid_id')
        out = self.st.artist_info_by_name(self.valid_artist_name)
        self.assertIsInstance(out, dict)
    
    def test_track_info_by_id(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.track_info_by_id('no_valid_id')
        out = self.st.track_info_by_id(self.valid_track_id)
        self.assertIsInstance(out, dict)


    def test_track_info_by_name(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.track_info_by_name('no_valid', 'no_valid')
        out = self.st.track_info_by_name(self.valid_track_name, self.valid_artist_name)
        self.assertIsInstance(out, dict)


    def test_tracks_by_artist_id(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.tracks_by_artist_id('')
        out = self.st.tracks_by_artist_id(self.valid_artist_id)
        self.assertIsInstance(out, dict)
        self.assertIsInstance(out['tracks'], list)
        self.assertIsInstance(out['metadata'], dict)
        self.assertTrue(len(out['tracks']) != 0)
        self.assertTrue(len(out['metadata'].keys()) != 0)


    def test_tracks_by_artist_name(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.tracks_by_artist_name('not-valid')
        out_i = self.st.tracks_by_artist_id(self.valid_artist_id)
        out_n = self.st.tracks_by_artist_name(self.valid_artist_name)
        self.assertTrue(out_i.keys() == out_n.keys())


    def test_tracks_by_ids(self):
        out = self.st.tracks_by_ids([self.valid_track_id])
        self.assertIsInstance(out, dict)
        self.assertTrue(list(out.keys()) == ['tracks'])
        self.assertTrue(len(out['tracks']) == 1)
        


    def test_artists_by_ids(self):
        out = self.st.artists_by_ids([self.valid_artist_id])
        self.assertIsInstance(out, dict)
        self.assertTrue(list(out.keys()) == ['artists'])
        self.assertTrue(len(out['artists']) == 1)

    def test_tracks_by_names(self):
        out = self.st.tracks_by_names([self.valid_track_name], self.valid_artist_name)
        self.assertIsInstance(out, dict)
        self.assertTrue(list(out.keys()) == ['tracks'])
        self.assertTrue(len(out['tracks']) == 1)
    

    def test_artists_by_names(self):
        out_n = self.st.artists_by_names([self.valid_artist_name])
        out_i = self.st.artists_by_ids([self.valid_artist_id])
        self.assertIsInstance(out_n, dict)
        self.assertTrue(list(out_n.keys()) == ['artists'])
        self.assertTrue(len(out_n['artists']) == 1)
        self.assertTrue(out_n['artists'][0].keys() == out_i['artists'][0].keys())

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
            
