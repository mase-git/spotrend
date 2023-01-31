from spotrend.loader import *
from spotrend.pattern import *
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')


class Spotrend(metaclass=Singleton):

    def __init__(self, id=None, secret=None, redirect_uri=None):
        self.loader = Loader(id, secret, redirect_uri)

    def get_available_markets(self, version="v1") -> dict:
        return self.loader.get_available_resource("markets", version=version)

    def get_available_genres(self, version="v1") -> dict:
        return self.loader.get_available_resource("recommendations", "available-genre-seeds", version=version)

    def get_artist(self, artist_id: str, version="v1") -> dict:
        return self.loader.get_resource(artist_id, "artists", version=version)

    def get_track(self, track_id: str, market=None, version="v1") -> dict:
        query = {}
        if market != None:
            query['market'] = market
        return self.loader.get_resource(track_id, "tracks", queries=query, version=version)

    def get_album(self, album_id: str, market=None, version="v1") -> dict:
        query = {}
        if market != None:
            query['market'] = market
        return self.loader.get_resource(album_id, "albums", queries=query, version=version)

    def get_playlist(self, playlist_id, additional_type=None, fields=None, market=None, version="v1") -> dict:
        query = {}
        if additional_type != None and additional_type.lower() in ("track", "episode"):
            query["additional_type"] = additional_type.lower()
        if fields != None and self._field_regex(fields):
            query['fields'] = fields.lower()
        if market != None:
            query['market'] = market
        return self.loader.get_resource(playlist_id, "playlists", queries=query, version=version)

    def _field_regex(self, fields: str) -> bool:
        # limited control caused by pumping-lemma
        pattern = re.compile(r"(\w+\.)?\w+\(\w+(\,\w+)*\)")
        return bool(pattern.match(fields))
