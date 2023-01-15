
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


class Spotrends():

    def __init__(self, offset=0, limit=1, client_id=None, client_secret=None):
        self._client_id = _client_id
        self._client_secret = _client_secret
        if client_id is not None:
            self._client_id = client_id
        if client_secret is not None:
            self._client_secret = client_secret
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
                                        client_id=self._client_id, client_secret=self._client_secret)
        self._sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.offset = 0
        self.limit = 1


    def oauth2(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
                                        client_id=self._client_id, client_secret=self._client_secret)
        self._sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    def artist_info_by_id(self, artist_id: str):
        if artist_id is None:
            logging.warning('artist_info_id() call with None artist_id could return void data.')
            return None
        try:
            raw = self._sp.artist(artist_id)
            logging.info('Retrieve artist information for the id: ' +  artist_id)
            return self._format('artist', raw)
        except spotipy.exceptions.SpotifyException: 
            raise SpotrendsInputException('Id ' + artist_id + ' invalid. Try with another value.')


    def artist_info_by_name(self, artist_name : str):
        return self.artist_info_by_id(self.artist_id_by_name(artist_name))

    
    def track_info_by_id(self, track_id : str):
        if track_id is None:
            logging.warning('track_info_by_id() call with None track_id could return void data.')
            return None
        try:
            raw = self._sp.track(track_id)
            logging.info('Retrieve track information for the id: ' + track_id)
            return self._format('track', raw)
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException('Id ' + track_id + ' invalid. Try with another value.')


    def track_info_by_name(self, track_name : str, artist_name : str):
        if track_name is None or artist_name is None:
            logging.warning('The track and related artist name must be specified in input or the result will be None.')
            return None
        return self.artist_info_by_id(self.track_id_by_name(track_name, artist_name))


    def tracks_by_artist_id(self, artist_id : str, limit=10, offset=0):
        if artist_id is None:
            logging.warning('tracks_by__artists_id() call with None artist_id could return void data.')
            return None
        if limit > 50:
            logging.warning('Limit exceed. Maximum value is 50.')
            raise SpotrendsInputException('Limit exceed. Maximum value is 50.')
        artist_name = self.artist_name_by_id(artist_id)
        raw = self._sp.search(artist_name, limit=limit, offset=offset)
        data = {"tracks" : [self._format('track', track) for track in raw['tracks']['item']]}
        # adding artist metadata for information binding 
        data['metadata'] = {'lenght' : len(data['tracks']), 'type' : 'track', 'artist_name' : artist_name, 'artist_id' : artist_id}
        return data


    def tracks_by_artist_name(self, artist_name : str, limit=10, offset=0):
        artist_id = self.artist_id_by_name(artist_name)
        return self.tracks_by_artist_id(artist_id, limit=limit, offset=offset)


    def tracks_by_ids(self, tracks_ids : list):
        data = {'tracks' : []}
        for id in tracks_ids:
            try:
                data['tracks'].append(self.track_info_by_id(id))
            except SpotrendsInputException:
                logging.warning('The id ' + id + ' is unreachable or invalid. Please provides a correct one.')
            finally:
                return data


    def artists_by_ids(self, artists_ids : list):
        data = {'artists' : []}
        for id in artists_ids:
            try:
                data['artists'].append(self.artist_info_by_id(id))
            except SpotrendsInputException:
                logging.warning('The id ' + id + ' is unreachable or invalid. Please provides a correct one.')
            finally:
                return data


    def tracks_by_names(self, tracks_names : list, artist_name : str):
        if artist_name is None or tracks_names is None or len(tracks_names) == 0:
            logging.warning('Invalid input value return always a void dictionary.')
            return {}
        return {'tracks' : [self.track_info_by_name(track_name=name, artist_name=artist_name) for name in tracks_names]}
    

    def artists_by_names(self, artists_name : list):
        if artists_name is None or len(artists_name) == 0:
            logging.warning('Invalid input, you must specified a no void list of artists names or the output is None.')
            return None
        return {'artists' : [self.artist_info_by_name(name) for name in artists_name]}
   

    def album_info_by_id(self, album_id : str):
        if album_id is None:
            logging.warning('track_info_by_id() call with None track_id could return void data.')
            return None
        try:
            raw = self._sp.album(album_id)
            logging.info('Retrieve album information for the id: ' + album_id)
            return self._format('album', raw)
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException('Id ' + album_id + ' invalid. Try with another value.')


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
        if artist_name is None:
            logging.warning('Can\'t retrievee the id if the artist name has a None value.')
            return None
        info = self._sp.search(q='artist:' + artist_name, type='artist')
        try:
            return str(info['artists']['items'][0]['id'])
        except IndexError:
            raise SpotrendsInputException('The artist ' + artist_name + ' doesn\'t exists. Error on the id extraction.')
    

    def artist_name_by_id(self, artist_id : str):
        if artist_id == None:
            logging.warning('artist_name_by_id() calls with None artist_id could return void data.')
            return None
        try:
            info = self._sp.artist(artist_id=artist_id)
            return info['name']
        except ValueError:
            raise SpotrendsInputException('The artist id ' + artist_id + ' unreachable')
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException('Invalid artist id: ' + artist_id + '. Try with another one.')


    def track_id_by_name(self, track_name : str, artist_name : str):
        if track_name is None or artist_name is None:
            logging.warning('Can\'t retrieve the track id with artist name or track name with None value.')
            return None
        try:
            info = self._sp.search(q=f"artist:{artist_name} track:{track_name}", type='track',offset=self.offset, limit=self.limit)
            return info['tracks']['items'][0]['id']
        except IndexError:
            raise SpotrendsInputException('The artist ' + artist_name + ' doesn\'t have a track named ' + track_name + '. Error on the id extraction.')
    

    def album_name_by_id(self, album_id : str):
        if album_id is None:
            logging.warning('Can\'t retrieve the album with null id, the result is None.')
            return None
        try:
            info = self._sp.album(album_id=album_id)
            return info['name']
        except ValueError:
            raise SpotrendsInputException('The album id ' + album_id + ' unreachable')
        except spotipy.exceptions.SpotifyException:
            raise SpotrendsInputException('Invalid artist id: ' + album_id + '. Try with another one.')

    def album_id_by_name(self, album_name : str, album_artist : str):
        if album_name is None or album_artist is None:
            logging.warning('Can\'t retrieve id from album name or album artist with null value. The result is None')
    
    def _format(self, type : str, data : dict):
        sample = {}
        if type.lower() == 'album':
            sample['spotify_url'] = data['external_urls']['spotify']
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
            # sum the totaal duration_ms of the album
            sample['total_duration_ms'] = sum([x['duration_ms'] for x in sample['tracks']])
            return sample
        elif type.lower() == 'artist':
            sample['spotify_url'] = data['external_urls']['spotify']
            sample['followers'] = data['followers']['total']
            sample['genres'] = data['genres']
            sample['id'] = data['id']
            sample['image'] = data['images'][0]['url'] # the greatest one
            sample['name'] = data['name']
            sample['popularity'] = data['popularity']
            sample['type'] = data['type']
            sample['uri'] = data['uri']
            sample['url'] = data['external_urls'][0]['spotify']
            return data
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
            logging.error('Error type - mismatch type from raw data type, expected track, album or artist.')
            raise SpotrendsInputException('Error type data. Type parameter must be artist, track or album.')

if __name__ == '__main__':
    a_id = "spotify:artist:36QJpDe2go2KgaRleHCDTp"
    sp = Spotrends()
    print(sp.album_info_by_id("spotify:album:5yTx83u3qerZF7GRJu7eFk"))