from spotrend.client import *
from spotrend.pattern import *

load_dotenv()

_client_id = os.getenv("SPOTREND_CLIENT_ID")
_client_secret = os.getenv("SPOTREND_CLIENT_SECRET")

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')


class Spotrend(Loader, metaclass=Singleton):

    def __init__(self, client_id=_client_id, client_secret=_client_secret):
        super().__init__(client_id, client_secret)

    @authenticate
    def get_available_markets(self, version="v1") -> dict:
        return self.get_available_resource("markets", version=version)

    @authenticate
    def get_available_genres(self, version="v1") -> dict:
        return self.get_available_resource("recommendations", "available-genre-seeds", version=version)

    @authenticate
    def get_artist(self, artist_id : str, version="v1") -> dict:
        return self.get_resource(artist_id, "artists", version=version)
    
    @authenticate
    def get_track(self, track_id : str, market=None, version="v1") -> dict:
        query = {}
        if market != None:
            query = { "market" : market }
        return self.get_resource(track_id, "tracks", queries=query, version=version)

    @authenticate
    def get_album(self, album_id : str, market=None, version="v1") -> dict:
        query = {}
        if market != None:
            query = { "market" : market }
        return self.get_resource(album_id, "albums", queries=query, version=version)
    
