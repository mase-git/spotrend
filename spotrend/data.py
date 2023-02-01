scopes = (
    "ugc-image-upload",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "app-remote-control",
    "streaming",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public",
    "user-follow-modify",
    "user-follow-read",
    "user-read-playback-position",
    "user-top-read",
    "user-read-recently-played",
    "user-library-modify",
    "user-library-read",
    "user-read-email",
    "user-read-private",
)

items = (
    "albums",
    "artists",
    "shows",
    "episodes",
    "audiobooks",
    "chapters",
    "tracks",
    "playlists",
)

page = """
<html>
  <head>
    <style>
      body {
        background-color: #191414;
        color: white;
        font-family: "Spotify-Circular", sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }

      .message {
        background-color: #1DB954;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0px 0px 10px #191414;
      }

      h1 {
        margin: 0;
        font-size: 24px;
      }

      p {
        margin: 20px 0 0 0;
        font-size: 16px;
      }
    </style>
  </head>
  <body>
    <div class="message">
      <h1>Authorization Successful</h1>
      <p>You have successfully authorized the Spotify API for use for Spotrend analysis.</p>
    </div>
  </body>
</html>
"""

__all__ = ["items", "scopes", "page"]