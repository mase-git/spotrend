import logging
from spotrend.client import *
from spotrend.pattern import *
from spotrend.exceptions import *
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')


class Spotrend(metaclass=Singleton):

    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None, client: Client = None):
        self.client = client or Client(client_id, client_secret, redirect_uri)
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

    def get_available_devices(self):
        """
        Return an object with the list of available devices
        """
        return self.get_available_resource("/me/player/devices")

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

    def get_several_artists(self, artist_ids: list = []) -> dict:
        """
        Return an object with artist information
        - Parameters:
            - artist_ids (list) : list of urn, uri or id of the artists
        - Returns:
            - dict : collection of Spotify artist information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-artists
        """
        return self.get_several_resources(artist_ids, "artists")

    def get_track(self, track_id: str, market: str = None) -> dict:
        """
        Return an object with track information
        - Parameters:
            - track_id (str) : the urn, uri or id of the track
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : Spotify track information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-track
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_resource(track_id, "tracks", params=param)

    def get_several_tracks(self, track_ids: list, market: str = None) -> dict:
        """
        Return an object with track information
        - Parameters:
            - track_id (list) : list of urn, uri or id of the tracks
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : collection of Spotify track information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-tracks
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_several_resources(track_ids, "tracks", params=param)

    def get_album(self, album_id: str, market: str = None) -> dict:
        """
        Return an object with album information
        - Parameters:
            - album_id (str) : the urn, uri or id of the album
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : Spotify album information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-album
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_resource(album_id, "albums", params=param)

    def get_several_albums(self, album_ids: list, market: str = None) -> dict:
        """
        Return an object with album information
        - Parameters:
            - album_id (list) : list of urn, uri or id of the albums
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : collection of Spotify album information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-albums
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_several_resources(album_ids, "albums", params=param)

    def get_album_tracks(self, album_id: str, market: str = None, limit: int = 20, offset: int = 0) -> dict:
        params = {"limit": limit, "offset": offset}
        if market != None:
            params['market'] = market
        if limit < 0 or limit > 50:
            raise SpotrendQuotaError(
                'The limit of 50 exceeded. Please, try with another limit.')
        endpoint = f"https://api.spotify.com/{self.version}/albums/{album_id}/tracks"
        return self.client.make_request(endpoint, method="GET", params=params)

    def get_user_saved_albums(self, limit: int = 20, market: str = None, offset: int = 0) -> dict:
        params = {"limit": limit, "offset": offset}
        if market != None:
            params['market'] = market
        if limit < 0 or limit > 50:
            raise SpotrendQuotaError(
                'The limit of 50 exceeded. Please, try with another limit.')
        endpoint = f"https://api.spotify.com/{self.version}/me/albums"
        return self.client.make_request(endpoint, method="GET", params=params)

    def save_albums_for_current_user(self, album_ids: list = []) -> dict:
        data = {"ids": album_ids}
        params = data
        endpoint = f"https://api.spotify.com/{self.version}/me/albums"
        return self.client.make_request(endpoint, method="PUT", params=params, data=data)

    def remove_user_saved_album(self, album_ids: list = []) -> dict:
        data = {"ids": album_ids}
        params = data
        endpoint = f"https://api.spotify.com/{self.version}/me/albums"
        return self.client.make_request(endpoint, method="DELETE", params=params, data=data)

    def check_user_saved_albums(self, albums_ids: list = []) -> list:
        params = {"ids": albums_ids}
        endpoint = "https://api.spotify.com/v1/me/albums/contains"
        return self.client.make_request(endpoint, method="GET", params=params)

    def get_new_releases(self, country: str = None, limit: int = 20, offset: int = 0) -> dict:
        params = {"limit": limit, "offset": offset}
        if country != None:
            params['country'] = country
        if limit < 0 or limit > 50:
            raise SpotrendQuotaError(
                'The limit of 50 exceeded. Please, try with another limit.')
        endpoint = "https://api.spotify.com/v1/browse/new-releases"
        return self.client.make_request(endpoint, method="GET", params=params)

    def get_playlist(self, playlist_id, additional_type: str = None, fields: str = None, market: str = None) -> dict:
        """
        Return an object with playlist information
        - Parameters:
            - playlist_id (str) : the urn, uri or id of the playlist
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : Spotify album information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
        """
        param = {}
        if additional_type != None and additional_type.lower() in ("track", "episode"):
            param["additional_type"] = additional_type.lower()
        if fields != None and self._field_regex(fields):
            param['fields'] = fields.lower()
        if market != None:
            param['market'] = market
        return self.get_resource(playlist_id, "playlists", params=param)

    def get_several_playlists(self, playlist_ids: list = [], additional_type: str = None, fields: str = None, market: str = None) -> dict:
        """
        Return an object with playlist information
        - Parameters:
            - playlist_ids (list) : list of urn, uri or id of the playlist
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : collection of Spotify album information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-playlists
        """
        param = {}
        if additional_type != None and additional_type.lower() in ("track", "episode"):
            param["additional_type"] = additional_type.lower()
        if fields != None and self._field_regex(fields):
            param['fields'] = fields.lower()
        if market != None:
            param['market'] = market
        return self.get_several_resources(playlist_ids, "playlists", params=param)

    def get_episode(self, episode_id, market: str = None) -> dict:
        """
        Return an object with episode information
        - Parameters:
            - episode_id (str) : the urn, uri or id of the episode
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : Spotify episode information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-episode
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_resource(episode_id, "episodes", params=param)

    def get_several_episodes(self, episode_ids: list = [], market: str = None) -> dict:
        """
        Return an object with episode information
        - Parameters:
            - episode_id (list) : list of urn, uri or id of the episodes
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : collection of Spotify episode information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-episodes
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_several_resources(episode_ids, "episodes", params=param)

    def get_chapter(self, chapter_id, market: str = None) -> dict:
        """
        Return an object with chapter information
        - Parameters:
            - chapter_id (str) : the urn, uri or id of the chapter
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : Spotify chapter information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-chapter
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_resource(chapter_id, "chapters", params=param)

    def get_several_chapters(self, chapter_ids: list = [], market: str = None) -> dict:
        """
        Return an object with chapter information
        - Parameters:
            - chapter_id (list) : list of urn, uri or id of the chapters
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : collection of Spotify chapter information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-chapters
        """
        param = {}
        if market != None:
            param['market'] = market
        return self.get_several_resources(chapter_ids, "chapters", params=param)

    def get_single_category(self, category_id, country: str = None, locale: str = None):
        """
        Return an object with chapter information
        - Parameters:
            - category_id (str) : the urn, uri or id of the chapter
            - country (str) : optional parameter with an ISO 3166-1 alpha-2 country code. Provide this parameter to ensure that the category exists for a particular country.
            - locale (str) : optional parameter for desidered language, consisting of an  ISO 639-1 language code and an ISO 3166-1 alpha-2 country code, joined by an underscore. 
        - Returns:
            - dict : Spotify category information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-category
        """
        param = {}
        if country != None:
            param['country'] = country
        if locale != None:
            param['locale'] = locale
        return self.get_resource(category_id, "browse/categories", params=param)

    def get_profile(self):
        """
        Get current user profile info
        - Returns:
            - dict : the logged account profile information
        """
        endpoint = f"https://api.spotify.com/{self.version}/me"
        return self.client.make_request(endpoint, method="GET")

    @staticmethod
    def _field_regex(fields: str) -> bool:
        """
        Regex checker for the fields parameter available in some params
        """
        # limited control caused by pumping-lemma
        pattern = re.compile(r"(\w+\.)?\w+\(\w+(\,\w+)*\)")
        return bool(pattern.match(fields))

    def get_resource(self, lookup_id: str, type: str,  params: dict = {}) -> dict:
        """
        Fundamental method to retrieve a resource of a specific type with optional param
        - Parameters:
            - lookup_id (str): the lookup id of the resource
            - type (str): the type of the resource
            - params (dict): a dictionary key-value for the input param fields
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
        if endpoint[-1] == '?':
            endpoint = endpoint[:-1]
        return self.client.make_request(endpoint=endpoint, method="GET", params=params)

    def get_several_resources(self, lookup_ids: list[str], type: str, params: dict = {}) -> dict:
        """
        Fundamental method to retrieve a batch response on multiple resources request
        of a specific type with optional param
        - Parameters:
            - lookup_ids (list): the lookup ids related to the batch resources
            - type (str): the type of the resource
            - params (dict): a dictionary key-value for the input param fields
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
        elif len(lookup_ids) > 20:
            raise SpotrendQuotaError(
                'The maximum size of ids is 20 different items')
        endpoint = f"https://api.spotify.com/{self.version}/{type}"
        params['ids'] = lookup_ids
        return self.client.make_request(endpoint, method="GET", params=params)

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
        return self.client.make_request(endpoint, method="GET")
