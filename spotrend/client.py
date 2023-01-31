
from dotenv import load_dotenv
from functools import wraps
import logging
import base64
import datetime
import requests
import json
import os

from spotrend.type import *
from spotrend.exceptions import *

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        if not instance.id or not instance.secret:
            raise SpotrendAuthError(
                "Invalid user client credentials")
        return func(*args, **kwargs)
    return wrapper

class Client():

    def __init__(self, id=None, secret=None, redirect_uri=None):
        load_dotenv()
        self.id = id or os.getenv("SPOTREND_CLIENT_ID")
        self.secret = secret or os.getenv("SPOTREND_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("SPOTREND_REDIRECT_URI")

class AuthClient(Client):
    pass

class CredentialsClient(Client):

    def __init__(self, id=None, secret=None):
        super().__init__(id, secret)
        self.access_token = None
        self.access_token_expires = None
        self.access_token_did_expire = True
        self.scope = "default"
        self.version = "v1"
        self.access_token_url = "https://accounts.spotify.com/api/token"
        self.headers = None

    @authenticate
    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        id = self.id
        secret = self.secret
        client_creds = f"{id}:{secret}"
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
