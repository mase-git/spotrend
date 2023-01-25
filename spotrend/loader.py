
from spotrend.client import Client
from functools import wraps
import spotrend.exceptions
import requests
import json


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        spotify = args[0]
        if not spotify.authenticate():
            raise spotrend.exceptions.SpotrendAuthError(
                "Invalid user client credentials")
        return func(*args, **kwargs)
    return wrapper


class Loader(Client):

    def __init__(self, client_id, client_secret):
        super(self, Client(client_id, client_secret))

    @authenticate
    def get_resource(self, lookup_id: str, resource_type: str, version="v1") -> json:
        """
        Invocation of a GET function to retrieves resources using Spotify API.
        The resource type specified the type of the item to request.

        Parameters:
            lookup_id (str): The Spotify ID, URI or URL of the resource
            resource_type (str): The type of the resource, it can be artists, shows, episodes, audiobooks, 
                                 chapters, tracks, users, playlists.
            version (str): The current version of the resource. Default value is v1.

        Returns:
            json: The raw data in a json format

        Raises:
            SpotrendServerError: If the server endpoint is currently unreachable or there is internal error.
            SpotrendPermissionError: If the request has invalid credentials 
            SpotrendNotFound: If the requested resource doesn't exist
            SpotrendRequestError: For any other error type, with a specified status code

        Notes:
        This function is used to retrieves the main data from the Spotify API. The current resource types
        available are listed in the parameters section, any other specified resource types are not available for this
        function, check the documentation for more info.

        """
        version = version | self.version
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        return self._get(endpoint, headers)

    @staticmethod
    def _status(status_code):
        if status_code in range(200, 299):
            pass
        else:
            raise spotrend.exceptions.SpotrendRequestError(
                f"Invalid request with {status_code} status code.")

    def _get(self, endpoint, headers):
        r = requests.get(endpoint, headers=headers)
        Loader._status(r.status_code)
        return json.loads(r.text)


    def _post(self, endpoint, headers, data):
        r = requests.post(endpoint, headers, data)
        Loader._status(r.status_code)
        return json.loads(r.text)
