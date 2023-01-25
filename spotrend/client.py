
from dotenv import load_dotenv
import spotrend.exceptions
import loader
import logging
import requests
import base64
import datetime
import json

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')


class Client():

    def __init__(self, client_id, client_secret):
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
            raise spotrend.exceptions.SpotrendAuthError(
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
        data = loader.Loader._post(token_url, data=token_data, headers=token_headers)
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
            "Authorization": f"Bearer {access_token}"
        }
        return headers
