
from dotenv import load_dotenv
from functools import wraps
import logging
import base64
import datetime
import requests
import json
import os

from spotrend.exceptions import SpotrendAuthError, SpotrendInvalidDataError, SpotrendRequestError

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')

_client_id = os.getenv("SPOTREND_CLIENT_ID")
_client_secret = os.getenv("SPOTREND_CLIENT_SECRET")



class Client():

    def __init__(self, client_id=_client_id, client_secret=_client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expires = None
        self.access_token_did_expire = True
        self.version = "v1"
        self.access_token_url = "https://accounts.spotify.com/api/token"
        self.headers = None

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise SpotrendAuthError(
                "You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        """
        Returns the token headers for the API requests
        """
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        """
        Returs the token data for the API requests
        """
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        """
        Performs authorization call to retrieves the current 
        access token with the current expiration time and 
        expiration status.
        """
        token_url = self.access_token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, headers=token_headers, data=token_data)
        if r.status_code not in range(200, 299):
            raise SpotrendRequestError(
                f"Invalid request with {r.status_code} status code.")
        data = json.loads(r.text)
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # Spotify provides it in seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        """
        Gets the current access token, if it is expired, we request another one.
        This method is used to retrives a current valid access token for the Spotify API requests
        according to the authorization policies provided by the Spotify documentation.
        """
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires == None:
            self.perform_auth()
            return self.get_access_token()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        """
        Defines the header for a possible API resource requests.
        """
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        return headers


items = [
    "albums",
    "artists",
    "shows",
    "episodes",
    "audiobooks",
    "chapters",
    "tracks",
    "playlists",
]


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loader = args[0]
        if not loader.client_id or not loader.client_secret:
            raise SpotrendAuthError(
                "Invalid user client credentials")
        return func(*args, **kwargs)
    return wrapper


class Loader(Client):

    def __init__(self, client_id=_client_id, client_secret=_client_secret):
        super().__init__(client_id, client_secret)
        self.client_id = client_id
        self.client_secret = client_secret

    @authenticate
    def get_resource(self, lookup_id: str, type: str,  queries={}, version="v1") -> dict:
        endpoint = f"https://api.spotify.com/{version}/{type}/{lookup_id}?"
        if type not in items or lookup_id == None:
            raise SpotrendInvalidDataError('The type of data is invalid.')
        for name, value in queries.items():
            endpoint = f"{endpoint}&{name}={value}"
        headers = self.get_resource_header()
        if endpoint[-1] == '?':
            endpoint = endpoint[:-1]
        return Loader._get(endpoint, headers)

    @authenticate
    def get_several_resources(self, lookup_ids: list[str], type: str, queries={}, version="v1") -> dict:
        if len(lookup_ids) == 0 or type not in items:
            raise SpotrendInvalidDataError(
                'You need to specify a spotify ID, URI or URL.')
        first = lookup_ids.pop(0)
        endpoint = f"https://api.spotify.com/{version}/{type}?ids={first}"
        for lookup_id in lookup_ids:
            endpoint += f",{lookup_id}"
        for name, value in queries.items():
            endpoint = f"{endpoint}&{name}={value}"
        headers = self.get_resource_header()
        return Loader._get(endpoint, headers)

    @authenticate
    def get_available_resource(self, type: str, subpath="", version="v1") -> dict:
        endpoint = f"https://api.spotify.com/{version}/{type}/{subpath}"
        headers = self.get_resource_header()
        return Loader._get(endpoint, headers)

    @staticmethod
    def _status(response: dict):
        if response.status_code in range(200, 299):
            pass
        else:
            res = json.loads(response.text)
            message = f"Error {res['error']['status']} - {res['error']['message']}"
            raise SpotrendRequestError(message)

    @staticmethod
    def _get(endpoint, headers):
        r = requests.get(url=endpoint, headers=headers)
        Loader._status(r)
        return json.loads(r.text)

    @staticmethod
    def _post(endpoint, headers, data):
        r = requests.post(url=endpoint, headers=headers, data=data)
        Loader._status(r)
        return json.loads(r.text)

    @staticmethod
    def _put(endpoint, headers, data):
        r = requests.put(url=endpoint, headers=headers, data=data)
        Loader._status(r)
        return json.loads(r.text)
