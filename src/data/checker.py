class Checker:
    """
    A class used to validate data loaded from the Loader class on Spotify tracks.
    
    Attributes:
        tracks (List[Dict[str, Any]]): A list of tracks, where each track is a dictionary containing metadata about the track.
        track_features (List[Dict[str, Any]]): A list of track features, where each track feature is a dictionary containing audio feature data for a track.
        track_audio_analysis (List[Dict[str, Any]]): A list of track audio analysis, where each track audio analysis is a dictionary containing audio analysis data for a track.
    
    Methods:
        check_track_ids() -> Union[str, None]:
            Validates that all tracks have a valid ID.
        
        check_track_features() -> Union[str, None]:
            Validates that all track features are for a track that exists in the tracks list.
    """