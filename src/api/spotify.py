
import spotipy
import pandas as pd
# To access authorised Spotify data
from spotipy.oauth2 import SpotifyClientCredentials
from env import Environment

# setting credentials
client_id = Environment.spotipy_client_id
client_secret = Environment.spotipy_client_secret
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)

# global spotipy object
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Spotify:

    def __init__(self, mode: int, limit: int):
        self.limit = limit
        self.mode = 0

    def get_drive(self):
        """ returns the drive url for the artists dataset
            Parameters:
                - url - drive url for the artists dataset
        """
        return 'https://drive.google.com/uc?id=' + Environment.spotify_artist_names

    def get_artists(self):
        """ returns the list of artists names
            Parameters:
                - result - list of artists names 
        """
        return list(pd.read_csv(self.get_drive())['artist_name'])

    def get_data(self, artist_name : str):
        """ returns the list of tracks info related on the artist in input
            Parameters: 
                - result - the dataframe with tracks data of an artist. If no tracks or genre, return None
        """
        result = sp.search(artist_name)
        genre_a = []
        genre = []
        id = []
        name = []
        popularity = []
        if self.mode is 0:
            track = result['tracks']['items'][0]
            artist = sp.artist(track['artists'][0]['external_urls']['spotify'])
            try:
                genre_a = artist['genres'][0]
            except ValueError:
                genre_a = sp.album(track['album']['external_urls']['spotify'])['genres']
                if genre_a is []:
                    # if no genre are related to the artist, return None
                    return None
        results = sp.search(q=artist_name, limit=self.limit)
        tracks = results['tracks']['items']
        # if no tracks are related to the artist, return None
        if len(tracks) is 0:
            return None
        feat = {}
        features = [None]
        i = 0
        # initialize features attributes
        while features is [None]:
            features = sp.audio_features(tracks=[tracks[i]['id']])
            i += 1
        keys = features[0].keys()
        for key in keys:
            feat[key] = []
        # iterate over tracks
        for track in tracks:
            if artist_name in track['artists']:
                id.append(track['id'])
                name.append(track['name'])
                popularity.append(track['popularity'])
                genre.append(genre_a)
                features = sp.audio_features(tracks=[track['id']])[0]
                if features is None:
                    continue
                # update keys
                keys = features.keys()
                for track_feat in features:
                    for key in keys:
                        feat[key].append(track_feat[key])
        # generatee dataframe
        data = pd.DataFrame()
        data['id'] = id
        data['track_name'] = name
        data['artist_name'] = [artist_name for i in range(len(id))]
        for key in keys:
            data[key] = feat[key]
        # return the dataframe
        return data      
                

