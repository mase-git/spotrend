from spotrend.client import *
from spotrend.pattern import *
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')


class Spotrend(metaclass=Singleton):

    def __init__(self, id=None, secret=None, redirect_uri=None):
        self.client = Client(id, secret, redirect_uri)
        self.version = "v1"

    def get_available_markets(self) -> dict:
        """
        Return an object with the list of available markets
        """
        return self.get_available_resource("markets")

    def get_available_genres(self) -> dict:
        """
        Return an object with the list of available genres
        """
        return self.get_available_resource("recommendations/available-genre-seeds")

    def get_artist(self, artist_id: str) -> dict:
        """
        Return an object with artist information
        - Parameters:
            - artist_id (str) : the urn, uri or id of the artist
        - Returns:
            - dict : Spotify artist information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artist
        """
        return self.get_resource(artist_id, "artists")

    def get_track(self, track_id: str, market=None) -> dict:
        """
        Return an object with track information
        - Parameters:
            - track_id (str) : the urn, uri or id of the track
            - market (str) : optional parameter for data filtering on a specific market
        - Returns:
            - dict : Spotify track information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-track
        """
        query = {}
        if market != None:
            query['market'] = market
        return self.get_resource(track_id, "tracks", queries=query)

    def get_album(self, album_id: str, market=None) -> dict:
        """
        Return an object with album information
        - Parameters:
            - album_id (str) : the urn, uri or id of the album
            - market (str) : optional parameter for data filtering on a specific market
        - Returns:
            - dict : Spotify album information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-album
        """
        query = {}
        if market != None:
            query['market'] = market
        return self.get_resource(album_id, "albums", queries=query)

    def get_playlist(self, playlist_id, additional_type=None, fields=None, market=None) -> dict:
        """
        Return an object with playlist information
        - Parameters:
            - playlist_id (str) : the urn, uri or id of the playlist
            - market (str) : optional parameter for data filtering on a specific market
        - Returns:
            - dict : Spotify album information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
        """
        query = {}
        if additional_type != None and additional_type.lower() in ("track", "episode"):
            query["additional_type"] = additional_type.lower()
        if fields != None and self._field_regex(fields):
            query['fields'] = fields.lower()
        if market != None:
            query['market'] = market
        return self.get_resource(playlist_id, "playlists", queries=query)

    def _field_regex(self, fields: str) -> bool:
        """
        Regex checker for the fields parameter available in some queries
        """
        # limited control caused by pumping-lemma
        pattern = re.compile(r"(\w+\.)?\w+\(\w+(\,\w+)*\)")
        return bool(pattern.match(fields))

    def get_resource(self, lookup_id: str, type: str,  queries={}) -> dict:
        """
        Fundamental method to retrieve a resource of a specific type with optional query
        - Parameters:
            - lookup_id (str): the lookup id of the resource
            - type (str): the type of the resource
            - queries (dict): a dictionary key-value for the input query fields
        - Returns:
            - dict : object with information about the required resource
        - Documentation:
            - This method follows authorization flow with dynamic scope changing according
            to the type of the resource, if you want to check more, 
            go to the official Spotify API documentation:
            https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
        """
        endpoint = f"https://api.spotify.com/{self.version}/{type}/{lookup_id}?"
        if type not in items or lookup_id == None:
            raise SpotrendInvalidDataError('The type of data is invalid.')
        for name, value in queries.items():
            endpoint = f"{endpoint}&{name}={value}"
        headers = self.client.get_resource_header()
        if endpoint[-1] == '?':
            endpoint = endpoint[:-1]
        return self._call_api("get", endpoint, headers)

    def get_several_resources(self, lookup_ids: list[str], type: str, queries={}) -> dict:
        """
        Fundamental method to retrieve a batch response on multiple resources request
        of a specific type with optional query
        - Parameters:
            - lookup_ids (list): the lookup ids related to the batch resources
            - type (str): the type of the resource
            - queries (dict): a dictionary key-value for the input query fields
        - Returns:
            - dict : object with information about the required resource
        - Documentation:
            - This method follows authorization flow with dynamic scope changing according
            to the type of the resource, if you want to check more, 
            go to the official Spotify API documentation:
            https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
        """
        if len(lookup_ids) == 0 or type not in items:
            raise SpotrendInvalidDataError(
                'You need to specify a spotify ID, URI or URL.')
        first = lookup_ids.pop(0)
        endpoint = f"https://api.spotify.com/{self.version}/{type}?ids={first}"
        for lookup_id in lookup_ids:
            endpoint += f",{lookup_id}"
        for name, value in queries.items():
            endpoint = f"{endpoint}&{name}={value}"
        headers = self.client.get_resource_header()
        return self._call_api("get", endpoint, headers)

    def get_available_resource(self, type: str) -> dict:
        """
        Get available resources call API to retrieves the collection of possible
        values for a specific parameter
        - Parameters:
            - type (str): the type of the resource list, it can be recommendations/available-genre-seeds 
            or markets
        - Returns:
            - dict : an object with the list of available resource's items
        """
        endpoint = f"https://api.spotify.com/{self.version}/{type}"
        headers = self.client.get_resource_header()
        return self._call_api("get", endpoint, headers)

    @staticmethod
    def _call_api(method: str, endpoint: str, headers: dict, data=None) -> dict:
        method = method.lower()
        response = requests.api.request(
            method, endpoint, headers=headers, data=data)
        if response.status_code not in range(200, 299):
            err = json.loads(response.text)
            message = f"Error {err['error']['status']} - {err['error']['message']}"
            raise SpotrendRequestError(message)
        else:
            return json.loads(response.text)
