import unittest
from spotrend.exceptions import *
from spotrend.client import Loader


class LoaderTest(unittest.TestCase):

    def setUp(self):
        self.loader = Loader()

    def test_authentication(self):
        album_id = "4aawyAB9vmqN3uQ7FjRGTy"
        loader = Loader(None, None)
        with self.assertRaises(SpotrendAuthError):
            loader.get_resource(album_id, type="albums")

    def test_get_resource(self):
        album_id = "4aawyAB9vmqN3uQ7FjRGTy"
        with self.assertRaises(SpotrendInvalidDataError):
            # raise SpotrendInvalidDataError cases
            # case 1: null id 
            self.loader.get_resource(None, type="albums")
            # case 2: invalid type
            self.loader.get_resource(album_id, type="_")

    def test_get_several_resources(self):
        album_ids = "382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc".split(
            ',')
        albums = self.loader.get_several_resources(album_ids, "albums")
        self.assertIsInstance(albums, dict)

        if "albums" in albums.keys():
            n = len(albums['albums'])
            self.assertEqual(n, 3)

        # define the market for the query into the body of the request
        market = "US"
        albums = self.loader.get_several_resources(album_ids, "albums", {"market" : market})
        self.assertIsInstance(albums, dict)

        with self.assertRaises(SpotrendInvalidDataError):
            # raise SpotrendInvalidDataError cases
            # case 1: list with no ids
            self.loader.get_several_resources([], type="albums")
            # case 2: invalid type
            self.loader.get_several_resources(album_ids, type="_")


    def test_invalid_status(self):
        # try to retrieve album with invalid id
        with self.assertRaises(SpotrendRequestError) as context:
            # response is 400 in this case
            self.loader.get_resource('_', type="albums")
        
        self.assertEqual(str(context.exception), "Error 400 - invalid id")