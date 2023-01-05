from api.tracker import Tracker
from utils.checker import Checker
from utils.formatter import Formatter
import pandas as pd

# utils and api classes
tracker = Tracker()
loader = Formatter()
checker = Checker()

# initial dataframes for artists and tracks 
artists = tracker.retrieves_artists()
tracks = tracker.retrieves_tracks_from_artist()

# format the header of the artists like the tracks format
artists = loader.format_header(artists) 

# merge dataframes
df = pd.merge(tracks, artists, on='artist_name')

df.to_csv("./data/tracks.csv", index=False)
