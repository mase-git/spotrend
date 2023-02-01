import unittest
from spotrend.client import *
from spotrend.exceptions import *

class ClientTest(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_get_credentials(self):
        # remove temporal key
        self.client.id = None
        with self.assertRaises(SpotrendAuthError) as context:
            self.client.get_client_credentials()
        
        self.assertEqual("Invalid user client credentials", str(context.exception))
        # reset the client for other tests
        self.client = Client()
    
    def test_access_token(self):
        # when the client is started, we don't have token set,
        # we can easily get it from Spotify API automatically inside the access_token() method
        self.client = Client() # no token at this state
        token = self.client.get_access_token()
        # the client obtains and set directly the new token
        self.assertEqual(self.client.access_token, token)

