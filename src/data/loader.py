class Loader:
    """
    A class used to load data from Spotify about tracks and their features.
    
    Attributes:
        client_id (str): The client ID for the Spotify API.
        client_secret (str): The client secret for the Spotify API.
        redirect_uri (str): The redirect URI for the Spotify API.
        sp (spotipy.client.Spotify): The Spotipy client used to access the Spotify API.
    
    Methods:
        get_track_features(track_id: str) -> Dict[str, Any]:
            Retrieves the audio features for the track with the specified ID.
        
        get_track_audio_analysis(track_id: str) -> Dict[str, Any]:
            Retrieves the audio analysis for the track with the specified ID.
        
        get_tracks(track_ids: List[str]) -> List[Dict[str, Any]]:
            Retrieves the metadata for the tracks with the specified IDs.
    """
