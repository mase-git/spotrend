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

    def __init__(self):
        self.st = Spotrend()  # offset 0 and limit 1
        self.valid_artist_id = "2WX2uTcsvV5OnS0inACecP"
        self.valid_track_id = "6rqhFgbbKwnb9MLmUQDhG6"
        self.valid_album_id = "5MS3MvWHJ3lOZPLiMxzOU6"
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

def check_list_values(x: list, y: list):
    if len(x) != len(y):
        return False
    for i in range(len(x)):
        if x[i] != y[i]:
            return False
    return True


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


    def test_oauth2(self):
        st = Spotrend()
        st.oauth2(self.st._client_id, self.st._client_secret)
        self.assertTrue(check_credentials(st._client_id, st._client_secret))
    

    def test_artist_info(self):
        with self.assertRaises(SpotrendsInputException) as context_id:
            no_valid = str(10)
            self.st.artist_info_by_id(no_valid)

        self.assertFalse('this is broken' in str(context_id.exception))

        with self.assertRaises(SpotrendsInputException) as context_name:
            no_valid = str('_')
            self.st.artist_info_by_name(no_valid)

        self.assertFalse('this is broken' in str(context_name.exception))

        # void element on None id
        res = self.st.artist_info_by_id(None)
        self.assertIsNone(res)

        # void element on None name
        res = self.st.artist_info_by_name(None)
        self.assertIsNone(res)

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

        # void element on None id
        res = self.st.track_info_by_id(None)
        self.assertIsNone(res)

        # void element on None name
        res = self.st.track_info_by_name(None, None)
        self.assertIsNone(res)

        id_info = self.st.track_info_by_id(self.valid_track_id)
        self.assertIsInstance(id_info, dict)
        name = id_info["name"]
        is_true = name == "Speak To Me - 2011 Remastered Version"
        self.assertTrue(is_true)

        # check the same reference by the name info retrieval
        name_info = self.st.track_info_by_name(
            self.valid_track_name, self.valid_artist_name)
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
        name = self.st.artist_name_by_id(self.valid_artist_id)
        tracks_name = self.st.tracks_by_artist_name(name)

        # void element on None id
        res = self.st.tracks_by_artist_id(None)
        self.assertIsNone(res)

        # void element on None name
        res = self.st.tracks_by_artist_name(None)
        self.assertIsNone(res)
        
        # out limit
        with self.assertRaises(SpotrendsInputException) as context_limit:
            res = self.st.tracks_by_artist_id(self.valid_artist_id, limit=90)
        self.assertFalse('this is broken' in str(context_limit.exception))

        # check the same structure for both mode
        self.assertTrue(check_results(tracks_id, tracks_name))
        # identify the artist_name
        self.assertTrue(tracks_id['metadata']['artist_name']
                        == tracks_name['metadata']['artist_name'])

    def test_tracks_by_values(self):
        # retrieve the correct data
        result_id = self.st.tracks_by_ids([self.valid_track_id])
        self.assertIsInstance(result_id, dict)

        keys = list(result_id.keys())
        self.assertTrue(keys == ['tracks'])

        tracks_ids = result_id['tracks']

        n = len(tracks_ids)
        self.assertTrue(n == 1)

        # check the id of the retrieves information
        # we know that the input has only one track
        id = tracks_ids[0]['id']
        self.assertIsNotNone(id)  # check correct existence
        self.assertTrue(id == self.valid_track_id)

        # check invalid id into the input collection
        with self.assertRaises(SpotrendsInputException) as context_id:
            not_valid = '_'
            self.st.tracks_by_ids([not_valid])
        self.assertFalse('this is broken' in str(context_id.exception))

        # do the same for the by names
        result_name = self.st.tracks_by_names([self.valid_track_name], self.valid_artist_name)
        self.assertIsInstance(result_name, dict)

        keys = list(result_name.keys())
        self.assertEqual(keys, ['tracks'])

        tracks_names = result_name['tracks']
        self.assertIsNotNone(tracks_names)

        artist_name = tracks_names[0]['artist_name']
        track_name = tracks_names[0]['name']
        self.assertTrue(artist_name == self.valid_artist_name and track_name == self.valid_track_name)

        self.assertTrue(check_results(result_name, result_id))

        # check void result
        result = self.st.tracks_by_names([], self.valid_artist_name)
        self.assertEqual(result, {})


    def test_artists_by_values(self):
        # retrieve the correct data
        result_id = self.st.artists_by_ids([self.valid_artist_id])
        self.assertIsInstance(result_id, dict)

        keys = list(result_id.keys())
        self.assertTrue(keys == ['artists'])

        artists = result_id['artists']

        n = len(artists)
        self.assertTrue(n == 1)

        # check the id of the retrieves information
        # we know that the input has only one artist reference
        id = artists[0]['id']
        self.assertIsNotNone(id)  # check correct existence
        self.assertTrue(id == self.valid_artist_id)

        # check invalid id into the input collection
        with self.assertRaises(SpotrendsInputException) as context_id:
            not_valid = '_'
            self.st.artists_by_ids([not_valid])
        self.assertFalse('this is broken' in str(context_id.exception))
    
        # do the same for the by names
        result_name = self.st.artists_by_names([self.valid_artist_name])
        self.assertIsInstance(result_name, dict)

        keys = list(result_name.keys())
        self.assertEqual(keys, ['artists'])

        artists_names = result_name['artists']
        self.assertIsNotNone(artists_names)

        artist_name = artists_names[0]['name']
        self.assertTrue(artist_name == self.valid_artist_name)

        self.assertTrue(check_results(result_name, result_id))

        # check void result
        result = self.st.artists_by_names([])
        self.assertEqual(result, {})

    def test_tracks_by_names(self):
        void = self.st.tracks_by_names([], self.valid_artist_name)
        self.assertDictEqual(void, {})


        result = self.st.tracks_by_names(
            [self.valid_track_name], self.valid_artist_name)

        # check the dictionary type
        self.assertIsInstance(result, dict)

        # check keys
        keys = list(result.keys())
        self.assertTrue(keys == ['tracks'])

        tracks = result['tracks']
        # check the tracks length with one element
        self.assertTrue(len(tracks) == 1)

        # check the correct artist_name reference
        artist_name = tracks[0]['artist_name']
        self.assertTrue(artist_name == self.valid_artist_name)

        # check the name of the traack
        track_name = tracks[0]['name']
        self.assertTrue(track_name == self.valid_track_name)

    def test_album_info_by_value(self):
        with self.assertRaises(SpotrendsInputException) as context_id:
            not_valid = '_'
            self.st.album_info_by_id(not_valid)
        
        self.assertFalse('this is broken' in str(context_id.exception))

        result = self.st.album_info_by_id(self.valid_album_id)
        self.assertIsInstance(result, dict)

        # check id 
        id = result['id']
        self.assertEqual(id, self.valid_album_id)

        void = self.st.album_info_by_id(None)
        self.assertIsNone(void)

        # do the same controls for the name input
        result = self.st.album_info_by_name(self.valid_album_name, self.valid_artist_name)
        self.assertIsInstance(result, dict)

        # check album name
        name = result['name']
        self.assertEqual(name, self.valid_album_name)


    def test_albums_by_artist(self):

        with self.assertRaises(SpotrendsInputException) as context:
            not_valid = "_"
            self.st.albums_by_artist_id(not_valid)

        result_id = self.st.albums_by_artist_id(self.valid_artist_id)
        self.assertIsInstance(result_id, dict)
    
        # check structure
        albums = result_id['albums']
        self.assertIsNotNone(albums)
        
        # check collection
        self.assertIsInstance(albums, list)

        # check validity
        self.assertTrue(len(albums) != 0)

        result_name = self.st.albums_by_artist_name(self.st.artist_name_by_id(self.valid_artist_id))

        albums = result_name['albums']
        self.assertIsNotNone(albums)

        # check collectio
        self.assertIsInstance(albums, list)

        # check null cases
        id_void = self.st.albums_by_artist_id(None)
        name_void = self.st.albums_by_artist_name(None)
        self.assertIsNone(id_void)
        self.assertIsNone(name_void)

        # check limit
        with self.assertRaises(SpotrendsInputException) as context_limit:
            self.st.albums_by_artist_id(self.valid_artist_id, limit=70) # valid until 50
    
        self.assertFalse('this is broken' in str(context_limit.exception))
    
        # check equality
        albums_id = result_id['albums']
        album_name = result_name['albums']
        res = check_list_values(albums_id, album_name)
        self.assertTrue(res)


    def test_albums_by_ids(self):
        res = self.st.albums_by_ids([self.valid_album_id])
        self.assertIsInstance(res, dict)

        # check keys
        keys = list(res.keys())
        self.assertListEqual(keys, ['albums'])

        # check lenght
        albums = res['albums']
        self.assertTrue(len(albums) == 1)

        # check id reference
        sample = albums[0]
        self.assertEqual(sample['id'], self.valid_album_id)

    def test_available_markets(self):
        res = self.st.available_markets()
        self.assertTrue(len(res) > 0)

    def test_images_by_artists_id(self):
        res_id = self.st.images_by_artists_id([self.valid_artist_id])
        name = self.st.artist_name_by_id(self.valid_artist_id)
        res_name = self.st.images_by_artists_names([name])

        self.assertIsInstance(res_id, dict)
        self.assertIsInstance(res_name, dict)

        # check validity
        images = res_id['images']
        images_2 = res_name['images']
        self.assertIsNotNone(images)
        self.assertIsNotNone(images_2)

        # check keys
        keys = list(res_id.keys())
        self.assertListEqual(keys, ['images'])
    
        keys_2 = list(res_name.keys())
        self.assertListEqual(keys, keys_2)

        # check output lenght
        self.assertTrue(len(images) > 0)
        self.assertTrue(len(images_2) > 0)

        # check same cardinality
        self.assertTrue(len(images) == len(images_2))
    

    def test_features_by_track(self):
        id = self.st.track_id_by_name(self.valid_track_name, self.valid_artist_name)

        # check void
        void = self.st.features_by_track_id(None)
        void_2 = self.st.features_by_track_name(None, None)
        self.assertTrue(void == void_2 and void_2 == None)

        # retrieve info
        feat_name = self.st.features_by_track_name(self.valid_track_name, self.valid_artist_name)
        feat_id = self.st.features_by_track_id(id)

        # check structure
        res = check_results(feat_name, feat_id)
        self.assertTrue(res)



    def test_artist_id_name_change(self):
        # find the name
        name = self.st.artist_name_by_id(self.valid_artist_id)
        self.assertIsNotNone(name)

        # find the id
        id = self.st.artist_id_by_name(name)
        self.assertEqual(id, self.valid_artist_id)

        # check null case
        void = self.st.artist_id_by_name(None)
        void_2 = self.st.artist_name_by_id(None)
        self.assertTrue(void == void_2 and void_2 is None)

        # check invalid input
        invalid = '_'
        with self.assertRaises(SpotrendsInputException) as context_name:
            self.st.artist_id_by_name(invalid)
        
        with self.assertRaises(SpotrendsInputException) as context_id:
            self.st.artist_name_by_id(invalid)

        self.assertFalse('this is broken' in str(context_name.exception))
        self.assertFalse('this is broken' in str(context_id.exception))


    def test_track_id_name_change(self):

        # find the id
        id = self.st.track_id_by_name(self.valid_track_name, self.valid_artist_name)
        self.assertIsNotNone(id)

        # find the name
        name = self.st.track_name_by_id(id)
        self.assertEqual(name, self.valid_track_name)

        # check null case
        void = self.st.track_id_by_name(None, None)
        void_2 = self.st.track_name_by_id(None)
        self.assertTrue(void == void_2 and void_2 is None)

        # check invalid input
        invalid = '_'
        with self.assertRaises(SpotrendsInputException) as context_name:
            self.st.track_id_by_name(invalid, invalid)
        
        with self.assertRaises(SpotrendsInputException) as context_id:
            self.st.track_name_by_id(invalid)

        self.assertFalse('this is broken' in str(context_name.exception))
        self.assertFalse('this is broken' in str(context_id.exception))

