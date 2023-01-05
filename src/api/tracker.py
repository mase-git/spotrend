from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import spotipy


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

    def __init__(self):
        """
        Initializes a Tracker object.
        """
        self.artists_url = 'https://drive.google.com/file/d/1ER-uBsnffjsGRjheptpPTPh6VN3tegJ1/view?usp=sharing'
        self.artists_url = 'https://drive.google.com/uc?id=' + self.artists_url.split('/')[-2] # format the drive url
        self.limit = 10
        self.credentials_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(client_credentials_manager=self.credentials_manager)
        self.tracks = pd.DataFrame()

    def set_artists_url(self, url : str):
        """
        Set the url of the artists data source
        
        Args:
            url (str): The url of the data source of artists, it should be a .csv file
        """
        self.artists_url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]

    def get_artists_url(self):
        """
        Get the current url of the artists data source
        """
        return self.artists_url
    
    def retrieves_artists(self):
        """
        Retrieve the dataframe from the url specified in the artists_url attribute
        """
        return pd.read_csv(self.artists_url)

    def get_tracks(self):
        return self.tracks
    
    def set_tracks(self, tracks : pd.DataFrame):
        """
        Set the current tracks dataframe
        
        Args:
            tracks (pandas.DataFrame): The updated dataframe for the new collection of tracks
        """
        self.tracks = tracks
    
    def retrieves_tracks_from_artist(self):
        """
        Retrieve the track dataframe from the artists list given by the related attribute value
        """
        # tracks is the result dataframe from the data extrapolation
        tracks = {}
        cols = []
        # flag for the header setup in the tracks dataframe | True = not header, False = already set
        setup_header = True
        # self.artists_names = self.retrieves_artists()
        self.artists_names = ['Drake', 'Lady Gaga']
        for artist_name in self.artists_names:
            results = self.sp.search(q=artist_name, limit=self.limit)
            for _, t in enumerate(results['tracks']['items']):
                # adding temporal redudant artist name
                t['artist_name'] = artist_name
                cols.append(t)

        # appending columns to the tracks dictionary
        for i in range(len(cols)):
            col = cols[i]
            keys = col.keys()
            if setup_header:
                for key in keys:
                    tracks[key] = []
                setup_header = False
            for key in keys:
                tracks[key].append(col[key])

        # convert the dictionary to the dataframe format
        df = pd.DataFrame()
        for key in tracks.keys():
            df[key] = tracks[key]

        tracks = pd.DataFrame.from_dict(tracks)
        for column in tracks.columns:
            # removing references attributes
            if(type(tracks[column][0]) == dict):
                df.drop(column, inplace=True, axis=1)
        
        # artists reference is out of scope of work, we need only the name
        df.drop('artists', inplace=True, axis=1)

        # update the state of the tracks
        self.tracks = df
        return df







        