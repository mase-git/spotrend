from utils.checker import Checker
from utils.formatter import Formatter
from utils.spreadsheet import SpredsheetWriter
from tracker import Tracker
import pandas as pd
import sys

# main tracker
tracker = Tracker(limit=50)

# utilities objects
formatter = Formatter()
checker = Checker()
spreadsheet = SpredsheetWriter()

lst_artists = tracker.get_artists_names()
# generate the final merged dataframe
df = pd.DataFrame()
frame = []
num = 0
total = len(lst_artists)

# iteration on artists to find the relative tracks
for artist in lst_artists:
    try:
        tracks = tracker.get_artist_tracks(artist)
    except:
        tracks = None
    if tracks is None:
        # tracks not valid or with no Spotify analysis available
        print(f'[Loading] => {num + 1}/{total} :: Tracks not ready for the {artist} author.')
    else:
        frame.append(tracker.get_artist_tracks(artist))
        print(f'[Loading] => {num + 1}/{total} :: Tracks saved for the {artist} author.')
    num += 1

# check the void frame
if frame == []:
    print('[Error] => No tracks detected.')
    sys.exit(0)

# concatenate the merged df
df = pd.concat(frame)
try:
    spreadsheet.generated_by_sheet_tags(df)
except:
    print('[Error] => Error during the spreadsheet generation')




