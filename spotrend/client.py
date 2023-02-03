import logging
import base64
import requests
import os
import json
import urllib
import webbrowser
from dotenv import load_dotenv
from functools import wraps
from six import b 
from six.moves import BaseHTTPServer
from spotrend.items import *
from spotrend.exceptions import *
from spotrend.pattern import *


logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        if not instance.client_id or not instance.client_secret:
            raise SpotrendAuthError(
                "Invalid user client credentials")
        return func(*args, **kwargs)
    return wrapper


class ServerAuthHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        """ GET Request handler for the callback localhost after Spotify authorization login """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b(page))
        self.server.authorization_code = urllib.parse.parse_qs(
            urllib.parse.urlparse(self.path).query)["code"][0]
        self.server.server_close()


class ServerAuth(BaseHTTPServer.HTTPServer, metaclass=Singleton):

    def __init__(self):
        self.port = 8080
        self.request_handler = ServerAuthHandler
        self.authorization_code = None
        try:
            BaseHTTPServer.HTTPServer.__init__(
                self, ('localhost', self.port), self.request_handler)
        except:
            raise SpotrendServerError(
                f'Cannot initialize a local server instance. Port {self.port} is busy.')

    def start(self):
        """
        Handle requests from localhost applying the ServerAuthHandler to retrieves the auth code.
        """
        self.handle_request()


class Client(metaclass=Singleton):

    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None):
        load_dotenv()
        self.client_id = client_id or os.getenv('SPOTREND_CLIENT_ID')
        self.client_secret = client_secret or os.getenv(
            'SPOTREND_CLIENT_SECRET')
        self.redirect_uri = redirect_uri or os.getenv('SPOTREND_REDIRECT_URI')
        self.token_file = "token.json"
        self.token = None
        self.scope = ' '.join(list(scopes))
        self.authorization_code = None
        self.server = ServerAuth()
        self.oauth2()


    @authenticate
    def get_authorization_url(self) -> str:
        """
        Get the authorization URL for the Spotify API.
        """

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }
        url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
        return url

    def get_resource_header(self):
        if self.token is None or int(self.token["expires_in"]) <= 0:
            self.refresh_token()

        headers = {
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        return headers

    def oauth2(self):
        """
        Begin the authorization flow with the request of the authorization code
        - Excepts:
            - SpotrendAuthError - in case there is some troubleshooting with the authentication in the client level
        """
        auth_url = self.get_authorization_url()
        webbrowser.open(auth_url)
        self.server.start()
        self.authorization_code = self.server.authorization_code
        self.request_token()

    def request_token(self) -> None:
        """
        Request an access token for the Spotify API using the authorization code.
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}"
        }
        data = {
            "grant_type": "authorization_code",
            "code": self.authorization_code,
            "redirect_uri": self.redirect_uri
        }
        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data)
        print(response.text)
        if response.status_code == 200:
            self.token = response.json()
            with open(self.token_file, "w") as f:
                json.dump(self.token, f)
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}")

    def refresh_token(self) -> None:
        """
        Refresh the access token for the Spotify API.
        """
        if self.token is None:
            self.request_token()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.token["refresh_token"]
        }
        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data)
        if response.status_code == 200:
            self.token = response.json()
            with open(self.token_file, "w") as f:
                json.dump(self.token, f)
        else:
            raise Exception(
                f"Refresh failed with status code {response.status_code}")

    def make_request(self, endpoint: str, method: str = "GET", params: dict = None, data: dict = None) -> dict:
        """
        Make a request to the Spotify API.
        """
        if self.token is None or int(self.token["expires_in"]) <= 0:
            self.refresh_token()

        headers = {
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        url = f"https://api.spotify.com/v1/{endpoint}"
        response = requests.request(
            method, url, headers=headers, params=params, json=data)
        if response.status_code == 401:
            self.refresh_token()
            headers = {
                "Authorization": f"Bearer {self.token['access_token']}"
            }
            response = requests.request(
                method, url, headers=headers, params=params, json=data)
        if response.status_code == 200:
            return response.json()
        print(response)
        return response.json()
