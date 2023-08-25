import codecs
import spotipy
import time
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

TOKEN_INFO = "token_info"

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


@app.route('/convert', methods=["GET", "POST"])
def convert():
    id = request.form.get("id")
    print(id)
    return 'all good'


@app.route('/result')
def displayResult():
    pass

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

def change_size(url, size):
    parts = url.split("/", 4)

    if len(parts) >= 4:
        parts[3] = str(size)
        new_url = '/'.join(parts)
        return new_url