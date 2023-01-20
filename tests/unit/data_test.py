import unittest
import spotipy
import os
from spotrend.client import Spotrend
from spotrend.exceptions import SpotrendsInputException
from dotenv import load_dotenv

# load dotenv
load_dotenv()

# setting credentials
_client_id = os.getenv("spotipy_client_id")
_client_secret = os.getenv("spotipy_client_secret")


class Environment():

    """
    Simulation environment with some id examples
    """

    def __init__(self):
        self.st = Spotrend()  # offset 0 and limit 1
        self.valid_artist_id = "spotify:artist:2WX2uTcsvV5OnS0inACecP"
        self.valid_track_id = "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
        self.valid_album_id = "spotify:album:5MS3MvWHJ3lOZPLiMxzOU6"
        self.valid_artist_name = "Drake"
        self.valid_track_name = "Rich Flex"
        self.valid_album_name = "Her Loss"


def check_keys(c: dict, d: dict) -> bool:
    k_c = set(list(c.keys()))
    k_d = set(list(d.keys()))
    return k_c == k_d


def check_values(c: dict, d: dict) -> bool:
    v_c = list(c.values())
    v_d = list(c.values())
    if len(v_c) != len(v_d):
        return False
    res = [v_c[i] == v_d[i] for i in range(len(v_c))]
    return not False in res


def check_results(c: dict, d: dict) -> bool:
    return check_values(c, d) and check_keys(c, d)


def check_credentials(id: str, secret: str) -> bool:
    if id is None or secret is None:
        return False
    st = Spotrend(client_id=id, client_secret=secret)
    return st._client_id == _client_id and st._client_secret == _client_secret


class SpotrendsTest(unittest.TestCase):

    def setUp(self):
        self.st = Spotrend()  # offset 0 and limit 1
        self.env = Environment()  # simulation environment variables

        # push variables to the current test
        self.valid_artist_id = self.env.valid_artist_id
        self.valid_track_id = self.env.valid_track_id
        self.valid_album_id = self.env.valid_album_id
        self.valid_artist_name = self.env.valid_artist_name
        self.valid_track_name = self.env.valid_track_name
        self.valid_album_name = self.env.valid_album_name

    def test_isIstance(self):

        # check invalid credentials
        self.st = Spotrend(offset=10, limit=20,
                           client_id='client_id', client_secret='client_secret')
        is_false = check_credentials(
            self.st._client_id, self.st._client_secret)
        self.assertFalse(is_false)

        # reinit instance for the setUp method
        self.st = Spotrend(limit=10, offset=10)

        # verify if the object is a correct instance of Spotrend
        self.assertIsInstance(self.st, Spotrend)

        # check valid credential
        is_true = check_credentials(self.st._client_id, self.st._client_secret)
        self.assertTrue(is_true)

    def test_artist_info(self):
        with self.assertRaises(SpotrendsInputException) as context_id:
            no_valid = str(10)
            self.st.artist_info_by_id(no_valid)

        self.assertFalse('this is broken' in str(context_id.exception))

        with self.assertRaises(SpotrendsInputException) as context_name:
            no_valid = str('_')
            self.st.artist_info_by_name(no_valid)

        self.assertFalse('this is broken' in str(context_name.exception))

        id_info = self.st.artist_info_by_id(self.valid_artist_id)
        self.assertIsInstance(id_info, dict)
        name = id_info["name"]
        is_true = name == 'Birdy'
        self.assertTrue(is_true)

        # check the same reference by the name info retrieval
        name_info = self.st.artist_info_by_name(name)
        is_true = name_info["id"] == id_info["id"]
        self.assertTrue(is_true)

        # check if the key-values of the dictionaries are the same
        is_true = check_results(name_info, id_info)
        self.assertTrue(is_true)

    def test_track_info(self):
        with self.assertRaises(SpotrendsInputException) as context_id:
            no_valid = str(10)
            self.st.track_info_by_id(no_valid)

        self.assertFalse('this is broken' in str(context_id.exception))

        with self.assertRaises(SpotrendsInputException) as context_name:
            no_valid = str('_')
            self.st.track_info_by_name(no_valid, no_valid)

        self.assertFalse('this is broken' in str(context_name.exception))

        id_info = self.st.track_info_by_id(self.valid_track_id)
        self.assertIsInstance(id_info, dict)
        name = id_info["name"]
        is_true = name == "Speak To Me - 2011 Remastered Version"
        self.assertTrue(is_true)

        # check the same reference by the name info retrieval
        name_info = self.st.track_info_by_name(self.valid_track_name, self.valid_artist_name)
        id = name_info["id"]
        id_info = self.st.track_info_by_id(id)
        is_true = name_info["id"] == id_info["id"]
        self.assertTrue(is_true)

        # check if the key-values of the dictionaries are the same
        is_true = check_results(name_info, id_info)
        self.assertTrue(is_true)



    def test_tracks_by_artist(self):
        with self.assertRaises(SpotrendsInputException) as context_id:
            not_valid = str('_')
            self.st.tracks_by_artist_id(not_valid)

        self.assertFalse('this is broken' in str(context_id.exception))
    
        with self.assertRaises(SpotrendsInputException) as context_name:
            not_valid = str('_')
            self.st.tracks_by_artist_name(not_valid)
        
        self.assertFalse('this is broken' in str(context_name.exception))

        tracks_id = self.st.tracks_by_artist_id(self.valid_artist_id)
        


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
        out = self.st.tracks_by_names(
            [self.valid_track_name], self.valid_artist_name)
        self.assertIsInstance(out, dict)
        self.assertTrue(list(out.keys()) == ['tracks'])
        self.assertTrue(len(out['tracks']) == 1)

    def test_artists_by_names(self):
        out_n = self.st.artists_by_names([self.valid_artist_name])
        out_i = self.st.artists_by_ids([self.valid_artist_id])
        self.assertIsInstance(out_n, dict)
        self.assertTrue(list(out_n.keys()) == ['artists'])
        self.assertTrue(len(out_n['artists']) == 1)
        self.assertTrue(out_n['artists'][0].keys() ==
                        out_i['artists'][0].keys())

    def test_album_info_by_id(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.album_info_by_id('no_valid_id')
        out = self.st.album_info_by_id(self.valid_album_id)
        self.assertIsInstance(out, dict)

    def test_album_info_by_name(self):
        out = self.st.album_info_by_name(
            self.valid_album_name, self.valid_artist_name)
        self.assertIsInstance(out, dict)

    def test_albums_by_artist_id(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.albums_by_artist_id('')
        out = self.st.albums_by_artist_id(self.valid_artist_id)
        self.assertIsInstance(out, dict)
        self.assertIsInstance(out['albums'], list)
        self.assertTrue(len(out['albums']) != 0)

    def test_albums_by_artist_name(self):
        with self.assertRaises(SpotrendsInputException) as context:
            self.st.albums_by_artist_name('not-valid')
        out_i = self.st.albums_by_artist_id(self.valid_artist_id)
        out_n = self.st.albums_by_artist_name(self.valid_artist_name)
        self.assertTrue(out_i.keys() == out_n.keys())

    def test_albums_by_ids(self):
        out = self.st.albums_by_ids([self.valid_album_id])
        self.assertIsInstance(out, dict)
        self.assertTrue(list(out.keys()) == ['albums'])
        self.assertTrue(len(out['albums']) == 1)

    def test_available_markets(self):
        out = self.st.available_markets()
        self.assertTrue(len(out) > 0)

    def test_images_by_artists_id(self):
        out = self.st.images_by_artists_id([self.valid_artist_id])
        none = self.st.images_by_artists_id(None)
        self.assertIsNone(none)
        self.assertTrue(out != None)
        self.assertTrue(list(out.keys()) == ['images'])
        self.assertTrue(len(out['images']) > 0)

    def test_images_by_artists_names(self):
        out = self.st.images_by_artists_names([self.valid_artist_name])
        none = self.st.images_by_artists_names(None)
        self.assertIsNone(none)
        self.assertTrue(out != None)
        self.assertTrue(list(out.keys()) == ['images'])
        self.assertTrue(len(out['images']) > 0)

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
