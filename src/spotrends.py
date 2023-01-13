from dotenv import load_dotenv
import spotipy, os

# load .env
load_dotenv()

# setting credentials
client_id = os.getenv("spotipy_client_id")
client_secret = os.getenv("spotipy_client_secret")
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)

# global spotipy object
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Spotrends():

    def __init__(self):
        pass