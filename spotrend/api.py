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

    def get_artist_top_tracks(self, artist_id : str, market : str = None) -> dict:
        """
        Get Spotify catalog information about an artist's top tracks by country.
        - Parameters:
            - artist_id (str): urn, uri or id of the artist
            - market (str): optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict: a set of tracks from the input artist 
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-artist-top-tracks     
        """
        params = {}
        if market != None:
            params['market'] = market
        endpoint = f"https://api.spotify.com/{self.version}/artists/{artist_id}/top-tracks"
        return self.client.make_request(endpoint, method="GET", params=params)

    def get_artist_related_artist(self, artist_id : str) -> dict:
        """
            Get Spotify catalog information about artists similar to a given artist. 
            Similarity is based on analysis of the Spotify community's listening history.        
        - Parameters:
            - artist_id (str): urn, uri or id of the artist
        - Returns:
            - dict: a set of related artists from the input artist 
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artists-related-artists
        """
        endpoint = f"https://api.spotify.com/{self.version}/artists/{artist_id}/related-artists"
        return self.client.make_request(endpoint, method="GET")

    def get_album_tracks(self, album_id: str, market: str = None, limit: int = 20, offset: int = 0) -> dict:
        """
        Get Spotify catalog information about an album’s tracks. Optional parameters can be used to limit the number of tracks returned.
        - Parameters:
            - album_id (list) : list of urn, uri or id of the albums
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
            - limit (int): The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
            - offset (int): The index of the first item to return. Default: 0 (the first item). Use with limit to get the next set of items.
        - Returns:
            - dict : collection of Spotify album information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-albums
        """
        params = {"limit": limit, "offset": offset}
        if market != None:
            params['market'] = market
        if limit < 0 or limit > 50:
            raise SpotrendQuotaError(
                'The limit of 50 exceeded. Please, try with another limit.')
        endpoint = f"https://api.spotify.com/{self.version}/albums/{album_id}/tracks"
        return self.client.make_request(endpoint, method="GET", params=params)

    def get_user_saved_albums(self, limit: int = 20, market: str = None, offset: int = 0) -> dict:
        """
        Return the user saved albums 
        - Parameters:
            - limit (int): The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
            - market (str): optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict: collection of Spotify saved albums for the current logged user
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-users-saved-albums
        """
        params = {"limit": limit, "offset": offset}
        if market != None:
            params['market'] = market
        if limit < 0 or limit > 50:
            raise SpotrendQuotaError(
                'The limit of 50 exceeded. Please, try with another limit.')
        endpoint = f"https://api.spotify.com/{self.version}/me/albums"
        return self.client.make_request(endpoint, method="GET", params=params)

    def save_albums_for_current_user(self, album_ids: list = []) -> dict:
        """
        Save albums for the current user inside the "Your Music" libraries
        - Parameters:
          - album_ids (list): list of albums ids to save in the "Your Music" library
        - Returns:
            - dict:  The status code of the saving operation
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/save-albums-user
        """
        data = {"ids": album_ids}
        params = data
        endpoint = f"https://api.spotify.com/{self.version}/me/albums"
        return self.client.make_request(endpoint, method="PUT", params=params, data=data)

    def remove_user_saved_album(self, album_ids: list = []) -> dict:
        """
        Remove albums for the current user inside the "Your Music" libraries
        - Parameters:
          - album_ids (list): list of albums ids to save in the "Your Music" library
        - Returns:
            - dict:  The status code of the saving operation
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/save-albums-user
        """   
        data = {"ids": album_ids}
        params = data
        endpoint = f"https://api.spotify.com/{self.version}/me/albums"
        return self.client.make_request(endpoint, method="DELETE", params=params, data=data)

    def check_user_saved_albums(self, albums_ids: list = []) -> list:
        """
        Check if a collection of albums ids is inside the "Your Music" library of the current logged user
        - Parameters:
            - albums_ids: id of albums to check if exists inside the "Your Music" 
        - Returns:
            - list: collection of booleans with True or False that indicates if the i-th album is present or not
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/check-users-saved-albums
        """
        params = {"ids": albums_ids}
        endpoint = "https://api.spotify.com/v1/me/albums/contains"
        return self.client.make_request(endpoint, method="GET", params=params)

    def get_new_releases(self, country: str = None, limit: int = 20, offset: int = 0) -> dict:
        """
        Get a list of new album releases featured in Spotify (shown, for example, on a Spotify player’s “Browse” tab).
        - Parameters:
            - country (str): A country: an ISO 3166-1 alpha-2 country code. Provide this parameter if you want the list of returned items 
            to be relevant to a particular country. If omitted, the returned items will be relevant to all countries.
            - limit (int): The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
            - offset (int): The index of the first item to return. Default: 0 (the first item). Use with limit to get the next set of items.
        - Returns:
            - dict: A paged set of albums
       - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-new-releases
        """
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

    def save_episodes_for_current_user(self, episode_ids: list = []) -> bool:
        """
        Save one or more episodes for the current user
        - Parameters:
            - episode_ids (list) : list of urn, uri or id of the episodes
        - Returns:
            - bool : True if the operation was successful, False otherwise
        """
        params = {"ids": episode_ids}
        endpoint = "https://api.spotify.com/v1/me/episodes"
        return self.client.make_request(endpoint, method="PUT", params=params)
    
    def remove_user_saved_episodes(self, episode_ids: list = []) -> bool:
        """
        Remove one or more episodes for the current user
        - Parameters:
            - episode_ids (list) : list of urn, uri or id of the episodes
        - Returns:
            - bool : True if the operation was successful, False otherwise
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:
            https://developer.spotify.com/documentation/web-api/reference/#/operations/remove-user-saved-episodes
        """
        params = {"ids": episode_ids}
        endpoint = "https://api.spotify.com/v1/me/episodes"
        return self.client.make_request(endpoint, method="DELETE", params=params)
    
    def check_user_saved_episodes(self, episodes_ids: list = []) -> list:
        """
        Check one or more episodes for the current user
        - Parameters:
            - episodes_ids (list) : list of urn, uri or id of the episodes
        - Returns:
            - list : list of urn, uri or id of the episodes
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:
            https://developer.spotify.com/documentation/web-api/reference/#/operations/check-user-saved-episodes
        """
        params = {"ids": episodes_ids}
        endpoint = "https://api.spotify.com/v1/me/episodes/contains"
        return self.client.make_request(endpoint, method="GET", params=params)
        
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
    
    def get_user_saved_shows(self):
        """
        Get current user saved shows
        - Returns:
            - dict : the logged account profile information
        """
        endpoint = f"https://api.spotify.com/{self.version}/me/shows"
        return self.client.make_request(endpoint, method="GET")

    def get_show(self, show_id : str, market: str = None) -> dict:
        """
        Return an object with show information
        - Parameters:
            - show_id (str) : the urn, uri or id of the show
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code    
        - Returns:
            - dict : Spotify show information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-show
        """
        param = {}
        if market!= None:
            param['market'] = market
        return self.get_resource(show_id, "shows", params=param)
    
    def get_several_shows(self, show_ids: list = [], market: str = None) -> dict:
        """
        Return a list with show information
        - Parameters:
            - show_id (list) : list of urn, uri or id of the shows
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : collection of Spotify show information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-shows
        """
        param = {}
        if market!= None:
            param['market'] = market
        return self.get_several_resources(show_ids, "shows", params=param)
    
    def get_show_episodes(self, show_id : str, market: str = None) -> dict:
        """
        Return a list with episode of input showe
        - Parameters:
            - show_id (str) : the urn, uri or id of the show
            - market (str) : optional parameter for data filtering on a specific ISO 3166-1 alpha-2 country code
        - Returns:
            - dict : collection of Spotify show information
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at:  
            https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-shows-episodes
        """
        param = {}
        if market!= None:
            param['market'] = market
        return self.get_resource(f"{show_id}/episodes", "shows", params=param)
    
    def put_show_for_current_user(self, show_ids : list) -> bool:
        """
        Add a list of shows to the current user's saved shows
        - Parameters:
            - show_ids (list) : list of urn, uri or id of the shows
        - Returns: bool : True if successful 
        - Documentation:
            - If you want to check the structure of the response, check 
            the official Spotify API documentation at: 
            https://developer.spotify.com/documentation/web-api/reference/#/operations/add-shows-to-my-saved-shows
        """
        if len(show_ids) > 50:
            raise SpotrendQuotaError("The maximum number of shows is 50")
        return self.client.make_request(f"https://api.spotify.com/{self.version}/me/shows", method="PUT", params=json.dumps(show_ids))

    def delete_show_from_current_user(self, show_ids : list) -> bool:
        """
        Remove a list of shows from the current user's saved shows
        - Parameters:
            - show_ids (list) : list of urn, uri or id of the shows
        - Returns: 
            - bool : True if the request was successful
        - Documentation:
            - This method follows authorization flow with dynamic scope changing according
            to the type of the resource, if you want to check more, 
            go to the official Spotify API documentation:
            https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
        """
        if len(show_ids) > 50:
            raise SpotrendQuotaError("The maximum number of shows is 50")
        return self.client.make_request(f"https://api.spotify.com/{self.version}/me/shows", method="DELETE", params=json.dumps(show_ids)) != None

    def check_user_saved_shows(self, show_ids : list) -> list:
        """
        Check if a list of shows is in the current user's saved shows
        - Parameters:
            - show_ids (list) : list of urn, uri or id of the shows
        - Returns: 
            - list : list of boolean values, True if the show is in the user's saved shows
        - Documentation:
            - If you want to check the structure of the response, check the official Spotify API documentation:
            https://developer.spotify.com/documentation/web-api/reference/#/operations/check-users-saved-shows
        """
        if len(show_ids) > 50:
            raise SpotrendQuotaError("The maximum number of shows is 50")
        return self.client.make_request(f"https://api.spotify.com/{self.version}/me/shows/contains", method="GET", params=json.dumps(show_ids))
    
    @staticmethod
    def _field_regex(fields: str) -> bool:
        """
        Regex checker for the fields parameter available in some params
        """
        # limited control caused by pumping-lemma
        pattern = re.compile(r"(\w+\.)?\w+\(\w+(\,\w+)*\)")
        return bool(pattern.match(fields))

    def put_resource(self, resource_id: str, resource_type: str, params: dict = None) -> bool:
        """
        Fundamental method to put a resource of a specific type with optional parameters
        - Parameters:
            - resource_id (str): the urn, uri or id of the resource
            - resource_type (str): the type of the resource
            - params (dict): a dictionary key-value for the input param fields
        - Returns:
            - bool : True if the request was successful
        - Documentation:
            - This method follows authorization flow with dynamic scope changing according
            to the type of the resource, if you want to check more, 
            go to the official Spotify API documentation:
            https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
        """
        endpoint = f"https://api.spotify.com/{self.version}/{resource_type}/{resource_id}?"
        if type not in items or resource_id == None:
            raise SpotrendInvalidDataError('The type of data is invalid.')
        if endpoint[-1] == '?':
            endpoint = endpoint[:-1]
        result : dict = self.client.make_request(endpoint=endpoint, method="PUT", params=params)
        return result != None
    
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

    def put_several_resources(self, resource_ids: list, resource_type: str, params : dict = {}) -> bool:
        """
        Fundamental method to put several resources of a specific type with optional parameters
        - Parameters:
            - resource_ids (list): list of urn, uri or id of the resources
            - resource_type (str): the type of the resource
            - params (dict): a dictionary key-value for the input param fields
        - Returns:
            - bool : True if the request was successful
        - Documentation:
            - This method follows authorization flow with dynamic scope changing according
            to the type of the resource, if you want to check more, 
            go to the official Spotify API documentation:
            https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
        """
        if len(resource_ids) == 0 or type not in items:
            raise SpotrendInvalidDataError(
                'You need to specify a spotify ID, URI or URL.')
        elif len(resource_ids) > 20:
            raise SpotrendQuotaError(
                'The maximum size of ids is 20 different items')
        endpoint = f"https://api.spotify.com/{self.version}/{resource_type}"
        params['ids'] = resource_ids
        return self.client.make_request(endpoint, method="PUT", params=params) != None
        
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

