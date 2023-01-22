
from urllib.error import HTTPError
from dotenv import load_dotenv
import spotipy
import logging
import os

from spotrend.exceptions import SpotrendsInputException

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


class Spotrend():

    def __init__(self, offset=0, limit=1, client_id=None, client_secret=None):

        """
        Create Spotrend Client instance
        :param offset : int : number of element to exclude in the ordered output collection
        :param limit : int : number of result for collection output 
        :param client_id : str : id of the client for the spotipy credentials
        :param client_secret : str : secret key of the client for the spotify credentials
        """
        self._client_id = _client_id
        self._client_secret = _client_secret
        if client_id is not None:
            self._client_id = client_id
        if client_secret is not None:
            self._client_secret = client_secret
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
            client_id=self._client_id, client_secret=self._client_secret)
        self._sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        self.offset = 0
        self.limit = 1

    def oauth2(self, client_id, client_secret):
        """define  the oauth2 credentials for the Spotipy and Spotify API calls
            - Parameters:
                - client_id : str - the id of the client for the oauth2 authorization
                - client_secret : str - the secret key of the client for the oauth2 authorization
        """
        self._client_id = client_id
        self._client_secret = client_secret
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
            client_id=self._client_id, client_secret=self._client_secret)
        self._sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)

    def artist_info_by_id(self, artist_id: str):
        """return info about the artist with the id specified in input
            - Parameters:
                - artist_id : str - the id of the artist
        """
        if artist_id is None or artist_id == "":
            logging.error(
                'artist_info_id() call with None artist_id could return void data.')
            return None
        try:
            raw = self._sp.artist(artist_id)
            logging.info(
                'Retrieve artist information for the id: ' + artist_id)
            return self._format('artist', raw)
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException(
                'Id ' + artist_id + ' invalid. Try with another value.')

    def artist_info_by_name(self, artist_name: str):
        """return info about the artist with the name specified in input
            - Parameters:
                - artist_name : str - the name of the artist
        """
        if artist_name is None or artist_name == "":
            logging.error(
                'artist_info_name() call with None artist_name could return void data.')
            return None
        return self.artist_info_by_id(self.artist_id_by_name(artist_name))

    def track_info_by_id(self, track_id: str):
        """return info about the track with the id specified in input
            - Parameters:
                - track_id : str - the id of the track 
        """
        if track_id is None or track_id == "":
            logging.error(
                'track_info_by_id() call with None track_id could return void data.')
            return None
        try:
            raw = self._sp.track(track_id)
            logging.info('Retrieve track information for the id: ' + track_id)
            return self._format('track', raw)
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException(
                'Id ' + track_id + ' invalid. Try with another value.')

    def track_info_by_name(self, track_name: str, artist_name: str):
        """return info about the track with the name specified in input
            - Parameters:
                - track_name : str - the name of the track 
        """
        if track_name is None or artist_name is None:
            logging.warning(
                'The track and related artist name must be specified in input or the result will be None.')
            return None
        return self.track_info_by_id(self.track_id_by_name(track_name, artist_name))

    def tracks_by_artist_id(self, artist_id: str, limit=10, offset=0):
        """return a list of tracks info about the tracks of the artist id specified in input
            - Parameters:
                - artist_id : str - the id of the main artist of the list of tracks
                - limit : int - a limit for the cardinality of the output collection, defaault: 10
                - offset : int - offset to shift result collection by n units, default : 0
        """
        if artist_id is None:
            logging.warning(
                'tracks_by_artists_id() call with None artist_id could return void data.')
            return None
        if limit > 50:
            logging.warning('Limit exceed. Maximum value is 50.')
            raise SpotrendsInputException('Limit exceed. Maximum value is 50.')
        artist_name = self.artist_name_by_id(artist_id)
        raw = self._sp.search(q=artist_name, type='track',
                              limit=limit, offset=offset)
        data = {"tracks": [self._format('track', track)
                           for track in list(raw['tracks']['items'])]}
        # adding artist metadata for information binding
        data['metadata'] = {'lenght': len(
            data['tracks']), 'type': 'track', 'artist_name': artist_name, 'artist_id': artist_id}
        return data

    def tracks_by_artist_name(self, artist_name: str, limit=10, offset=0):
        """return a list of tracks info about the tracks of the artist name specified in input
            - Parameters:
                - artist_name : str - the name of the main artist of the list of tracks
                - limit : int - a limit for the cardinality of the output collection, defaault: 10
                - offset : int - offset to shift result collection by n units, default : 0
        """
        artist_id = self.artist_id_by_name(artist_name)
        return self.tracks_by_artist_id(artist_id, limit=limit, offset=offset)

    def tracks_by_ids(self, tracks_ids: list):
        """return a list of tracks info about the id of tracks given in input
            - Parameters:
                - tracks_ids : list - a collection of id related to the tracks 
        """
        data = {'tracks': []}
        tracks_ids = list(set(tracks_ids))
        for id in tracks_ids:
            try:
                data['tracks'].append(self.track_info_by_id(id))
            except HTTPError:
                raise SpotrendsInputException(
                    'Track id: ' + id + ' is invalid.')
        return data

    def artists_by_ids(self, artists_ids: list):
        """ return a list of artists info about the id of artists given in input
            - Parameters:
                - artists_ids : list - a collection of id related to the artists
        """
        data = {'artists': []}
        artists_ids = list(set(artists_ids))
        for id in artists_ids:
            try:
                data['artists'].append(self.artist_info_by_id(id))
            except HTTPError:
                raise SpotrendsInputException(
                    'Artist id: ' + id + ' is invalid.')
        return data

    def tracks_by_names(self, tracks_names: list, artist_name: str):
        """return a list of tracks info about the name of tracks and the related artist given in input
            - Parameters:
                - tracks_names : list - a collection of names related to the tracks 
                - artist_name : str - the name of the main artist who made the tracks, so the collection is strictly related to a single artist
        """
        if artist_name is None or tracks_names is None or len(tracks_names) == 0:
            logging.warning(
                'Invalid input value return always a void dictionary.')
            return {}
        tracks_names = list(set(tracks_names))
        return {'tracks': [self.track_info_by_name(track_name=name, artist_name=artist_name) for name in tracks_names]}

    def artists_by_names(self, artists_name: list):
        """return a list of artists info about the names of artists given in input
            - Parameters:
                - artists_names : list - a collection of names related to the artists
        """
        if artists_name is None or len(artists_name) == 0:
            logging.warning(
                'Invalid input, you must specified a no void list of artists names or the output is None.')
            return {}
        return {'artists': [self.artist_info_by_name(name) for name in artists_name]}

    def album_info_by_id(self, album_id: str):
        """ return info about the album with the id specified in input
            - Parameters:
                - album_id : str - the id of the album
        """
        if album_id is None:
            logging.warning(
                'track_info_by_id() call with None track_id could return void data.')
            return None
        try:
            raw = self._sp.album(album_id)
            logging.info('Retrieve album information for the id: ' + album_id)
            return self._format('album', raw)
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException(
                'Id ' + album_id + ' invalid. Try with another value.')

    def album_info_by_name(self, album_name: str, artist_name: str):
        """return info about the album with the name specified in input
            - Parameters:
                - album_name : str - the name of the album
        """
        return self.album_info_by_id(self.album_id_by_name(album_name, artist_name))

    def albums_by_artist_id(self, artist_id: str, limit=10, offset=0):
        """return info about the album with the artist id specified in input
            - Parameters:
                - artist_id : str - the id of the artist
                - limit : int - a limit for the cardinality of the output collection, defaault: 10
                - offset : int - offset to shift result collection by n units, default : 0
        """
        if artist_id is None:
            logging.warning(
                'tracks_by_artists_id() call with None artist_id could return void data.')
            return None
        if limit > 50:
            logging.warning('Limit exceed. Maximum value is 50.')
            raise SpotrendsInputException('Limit exceed. Maximum value is 50.')
        artist_name = self.artist_name_by_id(artist_id)
        source = self._sp.search(
            q=f'artist: artist_name', type='album', limit=limit, offset=offset)
        albums = source['albums']['items']
        ids = [albums[i]["id"] for i in range(len(albums))]
        data = {'albums': [self.album_info_by_id(id) for id in ids]}
        data['metadata'] = {'lenght': len(
            data['albums']), 'type': 'album', 'artist_name': artist_name, 'artist_id': artist_id}
        return data

    def albums_by_artist_name(self, artist_name: str, limit=10, offset=0):
        """return info about the album with the artist name specified in input
            - Parameters:
                - artist_name : str - the name of the artist
                - limit : int - a limit for the cardinality of the output collection, defaault: 10
                - offset : int - offset to shift result collection by n units, default : 0
        """
        artist_id = self.artist_id_by_name(artist_name)
        return self.albums_by_artist_id(artist_id, limit=limit, offset=offset)

    def albums_by_ids(self, albums_ids: list):
        """ return a list of albums info about the id of albums given in input
            - Parameters:
                - albums_ids : list - a collection of id related to the albums
        """
        data = {'albums': []}
        for id in albums_ids:
            try:
                data['albums'].append(self.album_info_by_id(id))
            except SpotrendsInputException:
                logging.warning(
                    'The id ' + id + ' is unreachable or invalid. Please provides a correct one.')
            finally:
                return data

    def available_markets(self):
        """return the list of available markets on Spotify
        """
        return self._sp.available_markets()['markets']

    def images_by_artists_id(self, artists_id: list):
        """return images info about the collection of artists ids specified in input
            - Parameters:
                - artist_id : list - the ids of the artists
        """
        if artists_id == None or len(artists_id) == 0:
            logging.error(
                'images_by_artists_id() call with None artists_id length equals to 0 or null list, it could return void data.')
            return None
        images = {}
        images["images"] = []
        for id in artists_id:
            data = self.artist_info_by_id(id)
            images["images"].append(
                {'image': data['image'], 'artist_name': data['name'], 'artist_id': data['id']})
        return images

    def images_by_artists_names(self, artists_names: list):
        """return images info about the collection of artists names specified in input
            - Parameters:
                - artist_names : list - the names of the artists
        """
        if artists_names == None or len(artists_names) == 0:
            logging.error(
                'images_by_artists_id() call with None artists_id length equals to 0 or null list, it could return void data.')
            return None
        return self.images_by_artists_id([self.artist_id_by_name(name) for name in artists_names])

    def features_by_track_id(self, track_id: str):
        """return features list related to a track id given in input
            - Parameters:
                - track_id : str - the id of the input track
        """
        if track_id is None:
            logging.warning(
                'features_by_track_id() call with null id returns always a None collection')
            return None
        try:
            name = self.track_name_by_id(track_id)
            if name is None:
                logging.warning(
                    'features_by_track_id() call with invalid id returns always a None collection')
                return None
            data = self._sp.audio_features(tracks=[track_id])[0]
            data["track_name"] = name
            return data
        except ValueError:
            logging.error('Invalid track id: ' + track_id +
                          '. Please, try with a valid value.')
            raise SpotrendsInputException(
                'Invalid track id: ' + track_id + '. Please, try with a valid value.')

    def features_by_track_name(self, track_name: str, artist_name: str):
        """return features list related to a track and artist name given in input
            - Parameters:
                - track_name : str - the id of the input track
                - artist_name : str - the id of the input artist
        """
        if track_name is None or artist_name is None:
            logging.warning(
                'features_by_track_name() call with null track or artist name returns always a None collection')
            return None
        try:
            track_id = self.track_id_by_name(track_name, artist_name)
            return self.features_by_track_id(track_id)
        except ValueError:
            logging.error(
                'Invalid track or artist name. Please, try with a valid value.')
            raise SpotrendsInputException(
                'Invalid track or artist name. Please, try with a valid value.')
        except spotipy.exceptions.SpotifyException:
            logging.error(
                'Invalid track or artist name. Please, try with a valid value.')
            raise SpotrendsInputException(
                'Invalid track or artist name. Please, try with a valid value.')

    def features_by_tracks_ids(self, tracks_ids: list):
        """return a list of features collections related to a list of track ids given in input
            - Parameters:
                - tracks_ids : list - the list of ids of the input tracks
        """
        if tracks_ids is None or len(tracks_ids) == 0:
            logging.warning(
                'features_by_tracks_ids() calls with null list returns always None element')
            return None
        features = {}
        for track_id in tracks_ids:
            try:
                features[track_id] = self.features_by_track_id(track_id)
            except SpotrendsInputException:
                logging.warning('Invalid data for the current id: ' + track_id)
                continue
        return features

    def artist_id_by_name(self, artist_name: str):
        """return the id of the artist given its name in input
            - Parameters:
                - artist_name : str - the name of the input artist
        """
        if artist_name is None:
            logging.warning(
                'Can\'t retrievee the id if the artist name has a None value.')
            return None
        info = self._sp.search(q='artist:' + artist_name, type='artist')
        try:
            return str(info['artists']['items'][0]['id'])
        except IndexError:
            raise SpotrendsInputException(
                'The artist ' + artist_name + ' doesn\'t exists. Error on the id extraction.')

    def artist_name_by_id(self, artist_id: str):
        """return the name of the artist given its id in input
            - Parameters:
                - artist_id : str - the id of the input artist
        """
        if artist_id == None:
            logging.warning(
                'artist_name_by_id() calls with None artist_id could return void data.')
            return None
        try:
            info = self._sp.artist(artist_id=artist_id)
            return info['name']
        except ValueError:
            raise SpotrendsInputException(
                'The artist id ' + artist_id + ' unreachable')
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException(
                'Invalid artist id: ' + artist_id + '. Try with another one.')

    def track_name_by_id(self, track_id: str):
        """return the name of the track given its id in input
            - Parameters:
                - track_id : str - the id of the input track
        """
        if track_id == None:
            logging.warning(
                'track_name_by_id() call with None artist_id could return void data.')
            return None
        try:
            info = self._sp.track(track_id)
            return info['name']
        except ValueError:
            raise SpotrendsInputException(
                'The track id ' + track_id + ' unreachable')
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException(
                'Invalid track id: ' + track_id + '. Try with another one.')

    def track_id_by_name(self, track_name: str, artist_name: str):
        """return the id of the track given its name and the name of the artist in input
            - Parameters:
                - track_name : str - the name of the input track
        """
        if track_name is None or artist_name is None:
            logging.warning(
                'Can\'t retrieve the track id with artist name or track name with None value.')
            return None
        try:
            info = self._sp.search(
                q=f"artist:{artist_name} track:{track_name}", type='track', offset=self.offset, limit=self.limit)
            return info['tracks']['items'][0]['id']
        except IndexError:
            raise SpotrendsInputException(
                'The artist ' + artist_name + ' doesn\'t have a track named ' + track_name + '. Error on the id extraction.')

    def album_name_by_id(self, album_id: str):
        """return the name of the album given its id in input
            - Parameters:
                - album_id : str - the id of the input album
        """
        if album_id is None:
            logging.warning(
                'Can\'t retrieve the album with null id, the result is None.')
            return None
        try:
            info = self._sp.album(album_id=album_id)
            return info['name']
        except ValueError:
            raise SpotrendsInputException(
                'The album id ' + album_id + ' unreachable')
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException(
                'Invalid artist id: ' + album_id + '. Try with another one.')

    def album_id_by_name(self, album_name: str, album_artist: str):
        """return the id of the album given its name and the artist name, who is owner of the album, in input
            - Parameters:
                - album_name: str - the name of the input album
                - album_artist : str - the name of the artist who made the album (the main artist not the featuring)
        """
        if album_name is None or album_artist is None:
            logging.warning(
                'Can\'t retrieve id from album name or album artist with null value. The result is None')
            return None
        try:
            info = self._sp.search(
                q=f'album: {album_name} artist: {album_artist}', type="album")
            return info['albums']['items'][0]['id']
        except IndexError:
            raise SpotrendsInputException(
                'The album name ' + album_name + ' with author ' + album_artist + ' unreachable')
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException(
                'Invalid album or artist name. Try with another one.')

    def _format(self, type: str, data: dict):
        """format the output of data according to the data type given in input
            - Parameters:
                - type : str - the type of the data, it could be album, artist or track
                - data : dict - the collection of data that need to be formatted
        """
        sample = {}
        if type.lower() == 'album':
            sample['spotify_url'] = data['external_urls']['spotify']
            sample['id'] = data['id']
            sample['name'] = data['name']
            sample['label'] = data['label']
            sample['popularity'] = data['popularity']
            sample['release_date'] = data['release_date']
            sample['total_tracks'] = data['total_tracks']
            sample['href'] = data['external_urls']['spotify']
            sample['tracks'] = []
            for item in data['tracks']['items']:
                sample_x = {}
                sample_x['track_name'] = item['name']
                sample_x['explicit'] = item['explicit']
                sample_x['artist_name'] = item['artists'][0]['name']
                sample_x['artist_id'] = item['artists'][0]['id']
                sample_x['uri'] = item['uri']
                sample_x['track_id'] = item['id']
                sample_x['duration_ms'] = item['duration_ms']
                sample['tracks'].append(sample_x)
            # sum the total duration_ms of the album
            sample['total_duration_ms'] = sum(
                [x['duration_ms'] for x in sample['tracks']])
            return sample
        elif type.lower() == 'artist':
            sample['followers'] = data['followers']['total']
            sample['genres'] = data['genres']
            sample['id'] = data['id']
            sample['image'] = data['images'][0]['url']  # the greatest one
            sample['name'] = data['name']
            sample['popularity'] = data['popularity']
            sample['type'] = data['type']
            sample['uri'] = data['uri']
            sample['url'] = data['external_urls']['spotify']
            return sample
        elif type.lower() == 'track':
            sample['spotify_url'] = data['external_urls']['spotify']
            sample['id'] = data['id']
            sample['name'] = data['name']
            sample['popularity'] = data['popularity']
            sample['type'] = data['type']
            sample['uri'] = data['uri']
            sample['duration_ms'] = data['duration_ms']
            sample['album_release_date'] = data['album']['release_date']
            sample['album_name'] = data['album']['name']
            sample['album_id'] = data['album']['id']
            sample['artist_id'] = data['artists'][0]['id']
            sample['artist_name'] = data['artists'][0]['name']
            sample['artist_uri'] = data['artists'][0]['uri']
            sample['url'] = data['external_urls']['spotify']
            sample['explicit'] = data['explicit']
            return sample
        else:
            logging.error(
                'Error type - mismatch type from raw data type, expected track, album or artist.')
            raise SpotrendsInputException(
                'Error type data. Type parameter must be artist, track or album.')

