
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
            raise spotrend.exceptions.SpotrendAuthError("Invalid user client credentials")
        return func(*args, **kwargs)
    return wrapper


class Loader(Client):

    def __init__(self, client_id, client_secret):
        super(self, Client(client_id, client_secret))

    @authenticate
    def get_resource(self, lookup_id, resource_type, version="v1"):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        Loader.get_status(r.status_code)
        return json.loads(r.text)

    @staticmethod
    def get_status(status_code):
        if status_code in range(200, 299):
            pass
        elif status_code in range(500, 599):
            raise spotrend.exceptions.SpotrendServerError("Internal server error")
        elif status_code == 401:
            raise spotrend.exceptions.SpotrendPermissionError("Invalid user client credentials")
        elif status_code == 404:
            raise spotrend.exceptions.SpotrendNotFoundError("Page not found")
        else:
            raise spotrend.exceptions.SpotrendRequestError(f"Invalid request with {status_code} status code.")
