import spotipy
import pandas as pd
from utils.checker import Checker
from spotipy.oauth2 import SpotifyClientCredentials
from environment import Environment as env

# credentials for the Spotify API usage, you must set SPOTIPY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Tracker():

    """
    A class used to retrieves track information using Spotipy library

    Attributes:
        artists_url (str): A string of the data source of the artists that we want to retrieves tracks
        limit (int): Number of tracks per artist, according to Spotify documentation the value is between 1 and 100
        credential_manager (spotify.oauth2.SpotifyClientCredentials): credentials from the environment, you must setup SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
        sp (spotipy): The Spotipy client used to access the Spotify API.
        tracks (pandas.DataFrame): Dataframe of tracks extracted via Spotify API.
    """

    def __init__(self, limit):
        """
        Initializes a Tracker object.
        """
        self.artists_url = env.env_artist_url
        self.artists_url = env.env_prefix_url + \
            self.artists_url.split('/')[-2]  # format the drive url
        self.limit = limit
        self.checker = Checker()

    def get_artists_names(self):
        """
        Retrieve the dataframe from the url specified in the artists_url attribute
        """
        artists = pd.read_csv(self.artists_url)
        return list(artists['Artist Name'])

    def get_artist_tracks(self, artist_name):
        """
        Retrieves the tracks given an artist name in input and return the relative dataframe

        Args:
            artist_name (str): it is the name of the artist to retrieves tracks
        """
        # Set up the Spotipy client with your Spotify API credentials
        # Search for the artist
        results = sp.search(q=artist_name, type='artist')
        artist = results['artists']['items'][0]

        # Get the artist's top tracks defined by the limit number
        top_tracks = sp.search(
            q=artist['name'], limit=self.limit)
        tracks = top_tracks['tracks']['items']

        # check if there is no data
        if len(tracks) == 0:
            return None

        # extraction of reference keys
        keys = tracks[0].keys()
        art_keys = tracks[0]['artists'][0].keys()
        alb_keys = tracks[0]['album'].keys()

        # manage references
        ref = {}
        ref['base'] = [key for key in keys if type(
            tracks[0][key]) != dict and type(tracks[0][key]) != list]
        ref['artists'] = [key for key in art_keys if type(
            tracks[0]['artists'][0][key]) != dict and type(tracks[0]['artists'][0][key]) != list]
        ref['album'] = [key for key in alb_keys if type(
            tracks[0]['album'][key]) != dict and type(tracks[0]['album'][key]) != list]

        # initialize data and columns 
        data = {}
        for reference in ['artists', 'album']:
            for key in ref[reference]:
                data[reference + ':' + key] = []
        for key in ref['base']:
            data[key] = []
        
        # appending columns to the final dataframe
        for track in tracks:
            if(self.checker.check_index(artist_name, track['artists'], 'name') == -1):
                continue
            for references in ['artists', 'album']:
                for key in ref[references]:
                    if references == 'artists':
                        # check the id 
                        index = self.checker.check_index(artist_name, track[references], 'name')
                        if index == -1:
                            raise ValueError(f'Track doesn\'t have {artist_name} in artists')
                        data[references + ':' + key].append(track[references][index][key])
                    else:
                        data[references + ':' + key].append(track[references][key])
            for key in ref['base']:
                data[key].append(track[key])
        # setup temporal pandas.DataFrame
        df = pd.DataFrame()
        for key in data.keys():
            df[key] = data[key]
    
        # check if there is different artist name from the input name
        if self.checker.check_commons(df, artist_name):
            raise ValueError(f'Track with unknown artist name.')

        # adding audio featuress
        try:
            features = sp.audio_features(tracks=list(df['id']))
            if features == [None]:
            # no analyzed tracks, invalid values
                return None

            keys = features[0].keys()
            feat = {}
            for key in keys:
                feat[key] = []
        
            for track_feat in features:
                for key in keys:
                    feat[key].append(track_feat[key])

            for key in keys:
                df['feat:' +key] = feat[key]
        
            return df
        except:
            return None

