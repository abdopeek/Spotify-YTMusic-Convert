import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_secret="2164e2c1c8414ef088cd5bba36082723", client_id="d375822b692049b1bd21207a48f1d256", redirect_uri="https://localhost:5000"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])