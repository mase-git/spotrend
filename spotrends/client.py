
from dotenv import load_dotenv
import spotipy
import logging
import os

from spotrends.exceptions import SpotrendsInputException

# load dotenv
load_dotenv()

# setup logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')
# setting credentials
_client_id = os.getenv("spotipy_client_id")
_client_secret = os.getenv("spotipy_client_secret")
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id=_client_id, client_secret=_client_secret)


class Spotrends():

    def __init__(self, offset : int, limit : int, client_id=None, client_secret=None):
        self._client_id = _client_id
        self._client_secret = _client_secret
        if client_id is not None:
            self._client_id = client_id
        if client_secret is not None:
            self._client_secret = client_secret
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
                                        client_id=_client_id, client_secret=_client_secret)
        self._sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.offset = 0
        self.limit = 1


    def artist_info_by_id(self, artist_id: str):
        raw = None
        data = {}
        if artist_id is None:
            logging.warning('artist_info() calls with None artist_name could return void dataframe.')
            return None
        try:
            raw = self._sp.artist(artist_id)
            logging.info(raw)
            data['spotify_url'] = raw['external_urls']['spotify']
            data['followers'] = raw['followers']['total']
            data['genres'] = raw['genres']
            data['id'] = raw['id']
            data['image'] = raw['images'][0]['url'] # the greatest one
            data['name'] = raw['name']
            data['popularity'] = raw['popularity']
            data['type'] = raw['type']
            data['uri'] = raw['uri']
            return data
        except spotipy.exceptions.SpotifyException: 
            raise SpotrendsInputException('Id ' + artist_id + ' invalid. Try with another value.')

    def artist_info_by_name(self, artist_name : str):
        return self.artist_info_by_id(self.artist_id_by_name(artist_name))

    
    def track_info_by_id(self, track_id : str):
        pass

    def track_info_by_name(self, track_name : str):
        pass

    def tracks_by_artist_id(self, artist_id : str, limit : str):
        pass

    def tracks_by_artist_name(self, artist_name : str):
        pass

    def tracks_by_ids(self, tracks_id : list):
        pass

    def artists_by_ids(self, artists_id : list):
        pass

    def tracks_by_names(self, tracks_names : list):
        pass

    def artists_by_names(self, artists_name : list):
        pass
   
    def album_info_by_id(self, track_id : str):
        pass

    def album_info_by_name(self, track_name : str):
        pass

    def album_by_artist_id(self, artist_id : str, limit : str):
        pass

    def album_by_artist_name(self, artist_name : str):
        pass

    def album_by_ids(self, tracks_id : list):
        pass

    def available_markets(self):
        return self.sp.available_markets()['markets']

    def images_by_artists_id(self, artists_id : list):
        pass

    def images_by_artists_names(self, artists_names : list):
        pass

    def features_by_track_id(self, track_id : str):
        pass

    def features_by_track_name(self, track_id : str):
        pass
    
    def features_by_track_ids(self, tracks_id : list):
        pass

    def features_by_tracks_names(self, tracks_id : list):
        pass

    def artist_id_by_name(self, artist_name : str):
        info = self._sp.search(q='artist:' + artist_name, type='artist')
        try:
            return str(info['artists']['items'][0]['id'])
        except IndexError:
            raise SpotrendsInputException('The artist ' + artist_name + ' doesn\'t exists. Error on the id extraction.')
            
    def track_id_by_name(self, track_name : str, artist_name : str):
        try:
            info = self._sp.search(q=f"artist:{artist_name} track:{track_name}", type='track',offset=self.offset, limit=self.limit)
            return info['tracks']['items'][0]['id']
        except IndexError:
            raise SpotrendsInputException('The artist ' + artist_name + ' doesn\'t have a track named ' + track_name + '. Error on the id extraction.')
    

