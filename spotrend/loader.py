import requests
from spotrend.client import *


class Loader():

    def __init__(self, id=None, secret=None, redirect_uri=None):
        self.cred_client = CredentialsClient(id, secret)
        self.auth_client = AuthClient(id, secret, redirect_uri)

    def get_resource(self, lookup_id: str, type: str,  queries={}, version="v1") -> dict:
        endpoint = f"https://api.spotify.com/{version}/{type}/{lookup_id}?"
        if type not in items or lookup_id == None:
            raise SpotrendInvalidDataError('The type of data is invalid.')
        for name, value in queries.items():
            endpoint = f"{endpoint}&{name}={value}"
        headers = self.cred_client.get_resource_header()
        if endpoint[-1] == '?':
            endpoint = endpoint[:-1]
        return self.call_api("get", endpoint, headers)


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
        headers = self.cred_client.get_resource_header()
        return self.call_api("get", endpoint, headers)


    def get_available_resource(self, type: str, subpath="", version="v1") -> dict:
        endpoint = f"https://api.spotify.com/{version}/{type}/{subpath}"
        headers = self.cred_client.get_resource_header()
        return self.call_api("get", endpoint, headers)

    @staticmethod
    def call_api(method : str, endpoint : str, headers : dict, data=None):
        respose : requests.Response
        if method.lower() == "get":
            response = requests.get(url=endpoint, headers=headers, data=data)
        elif method.lower() == "post":
            response = requests.post(url=endpoint, headers=headers, data=data)
        elif method.lower() == "put":
            response = requests.put(url=endpoint, headers=headers, data=data)
        elif method.lower() == "delete":
            response = requests.delete(url=endpoint, headers=headers, data=data)
        else:
            raise SpotrendRequestError('Unsupported input HTTP method type')
        
        if response.status_code not in range(200, 299):
            err = json.loads(response.text)
            message = f"Error {err['error']['status']} - {err['error']['message']}"
            raise SpotrendRequestError(message)
        else:
            return json.loads(response.text)
          
