import google.oauth2.credentials
import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
import time
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

TOKEN_INFO = "token_info"
SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/youtube.force-ssl', 
            'https://www.googleapis.com/auth/youtubepartner']
CLIENT_SECRET_FILE = 
API_SERVICE_NAME = 'youtube'
API_VERSION = "v3"


app.secret_key = "DWN213moahr"
app.config['SESSION_COOKIE_NAME'] = 'luh cookie'

app.config["SESSION_PERMANENT"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = create_oauth()
    session.clear()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirectPage():
    sp_auth = create_oauth()
    session.clear()
    code = request.args.get('code')
    token_data = sp_auth.get_access_token(code)
    session[TOKEN_INFO] = token_data
    return redirect('/playlists')


@app.route('/playlists')
def getPlaylists():
    session[TOKEN_INFO], authorized = get_token()
    session.modified = True
    
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlists = sp.current_user_playlists()['items']
    res = []
    for playlist in playlists:
        p = {
            "name": playlist['name'],
            'image': playlist['images'][0]['url'],
            'tracks': playlist['tracks']['total'],
            'id': playlist['id']
        }
        res.append(p)
    return render_template('playlists.html', playlists=res)


@app.route('/googleConvert')
def googleConvert():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = url_for('googleConvert', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('convert'))




@app.route('/googleLogin')
def googleLogin():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES
    )
    flow.redirect_uri = url_for('googleConvert', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_access="true"
    )

    session['state'] = state

    return redirect(authorization_url)



@app.route('/convert', methods=["GET", "POST"])
def convert():
    id = request.form.get("id")
    session[TOKEN_INFO], authorized = get_token()
    session.modified = True
    
    if not id:
        return redirect('/playlists')
    elif not authorized:
        return redirect('/')
    elif 'credentials' not in session:
        return redirect('/googleLogin')
    # if not authorized:
    #     return redirect('/')
    # elif 'credentials' not in session:
    #     return redirect('/googleLogin')
    # elif not id:
    #     return redirect('/playlists')
    
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials']
    )

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlist = sp.playlist(id)

    youtube = create_youtube(credentials)
    yt_playlist = create_playlist(youtube, playlist)
    result = add_songs(youtube, playlist, yt_playlist)
    failed = [d for d in result if d.get('status') == False]


    return render_template('result.html', failed=failed)


@app.route('/result')
def displayResult():
    return render_template('result.html')

def get_token():
    valid_token = False
    token_data = session.get('token_info', {})

    if not (session.get('token_info', False)):
        valid_token = False
        return token_data, valid_token

    now = int(time.time())
    is_expired = session.get('token_info').get('expires_at') - now < 60

    if (is_expired):
        sp_oauth = create_oauth()
        token_data = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    valid_token = True
    return token_data, valid_token


def create_oauth():
    return SpotifyOAuth(
        client_id="d375822b692049b1bd21207a48f1d256",
        client_secret="2164e2c1c8414ef088cd5bba36082723",
        redirect_uri=url_for('redirectPage', _external=True),
        scope='playlist-read-private playlist-read-collaborative'
    )


def create_youtube(credentials):
    # Create YouTube OAuth and build
    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials
    )

    return youtube


def find_song(youtube, song_name):
    rqst = youtube.search().list(
        part='snippet',
        q=song_name,
        maxResults=3,
        type="video"
    )

    response = (rqst.execute())
    return response['items'][0]['id']['videoId']


def insert_song(youtube, yt_playlist, song_id):
    rqst = youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': yt_playlist['id'],
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': song_id
                }
            }
        }
    )

    response = (rqst.execute())
    if 'error' in response:
        return response['error']['message']
    return True


def add_songs(youtube, sp_playlist, yt_playlist):
    playlist = sp_playlist
    results = []
    for track in playlist['tracks']['items']:
        name = track['track']['name']
        artists = [artist['name'] for artist in track['track']['artists']]
        artists = ', '.join(artists)
        track_name = name + ' - ' + artists
        song_id = find_song(youtube, track_name)
        insertion = insert_song(youtube, yt_playlist, song_id)
        result = {
            'name':track_name,
            'result':insertion
        }
        results.append(result)

    return results


def create_playlist(youtube, sp_playlist):
    title = sp_playlist['name']
    rqst = youtube.playlists().insert(
        part="snippet, status",
        body={
            "snippet": {
                "title": title
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        }
    )

    response = (rqst.execute())
    if 'error' in response:
        raise Exception(f"Playlist not created: {response['error']['message']}")
    return response



def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}
