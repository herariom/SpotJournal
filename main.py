from flask import Flask, render_template, url_for, request, make_response
import os
from random import randrange
from werkzeug.utils import redirect

from chart import generate_chart
from forms import ContactForm, FinishedForm
import pymysql.cursors

from song_data import SongData

import spotipy, random, json, requests, string
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import SearchVideos

app = Flask(__name__)

sess_key = os.urandom(32)

# Generate session key
app.secret_key = sess_key

app.config['SECRET_KEY'] = sess_key
app.config['WTF_CSRF_ENABLED'] = False

labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Angry"]


# def generate_chart():
#     labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Unsure"]
#
#     testdata = []
#
#     user_values = [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)]
#     print(user_values)
#     testdata.append(SongData('Your Emotions', user_values, 220, 0, 0))
#
#     for x in range(1, 10):
#         testdata.append(SongData(('User ' + str(x)), [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)], randrange(30, 255, 5), randrange(30, 255, 5), randrange(30, 255, 5)))
#
#     return render_template('results.html', data=testdata, labels=labels)

def get_random_song():
  letters = string.ascii_lowercase
  random_string = ''.join(random.choice(letters) for i in range(10))
  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ca077b4c1b6b4ea7a33ed0069ec3eecb",
                client_secret="2d2baf7aa1ff4c9792822aefac0ef7e5",
                          redirect_uri="https://favorable-mark-297715.uc.r.appspot.com/form/before",
                          state = random_string,
                          scope="user-read-recently-played user-modify-playback-state user-read-private"))
  results = sp.current_user_recently_played(limit=50) # Dictionary of user's recently played tracks (@https://developer.spotify.com/console/get-recently-played/)
  user_id = sp.current_user()['id'] # Unique ID of Spotify User
  all_tracks = [] # Stores list of all the recently played tracks 

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # Make sure to create if condition that will repeat random selection if #
  # randomly selected song has already been played -> check database using#
  # unique user id and then check if it's in the list                     #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  for item in results['items']:
      track = item['track']
      all_tracks.append(track['name']+ ' - ' +track['artists'][0]['name'])
  random_song = random.choice(all_tracks)

  def findYTLink(search):
    # Function returns a YouTube link of the random_song in String datatype.
    words = search.split()
    api_key = "AIzaSyAvE4oj4Wb-UttuV4T6cf_zSi7mnw-ewuo"
    json_url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=" + "+".join(words) + "&type=video&key=" + api_key
    json_data = json.loads(requests.get(json_url).text)
    yt_id = json_data['items'][0]['id']['videoId']
    return yt_id
    #yt_link = "https://www.youtube.com/watch?v=" + yt_id
    #return yt_link

  # If the youtubesearch python module fails e.g search.result() returns an empty string
  # Then, use findYTLink to parse link using YouTube Data API v3
  search = SearchVideos(random_song, offset = 1, mode = "json", max_results = 1)
  if search.result() == None:
    url_id = findYTLink(random_song)
  else:
    result = json.loads(search.result())
    url_id = result['search_result'][0]['id']
  return "https://www.youtube.com/embed/" + url_id

@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('listen.html', url=url)
'''
@app.route('/form/finished', methods=('GET', 'POST'))
def post_questionnaire():
  form = PostForm()

  if request.method == 'POST' and form.validate_on_submit():
        if state == 'finished':

            return render_template('results.html', data=generate_chart(request.cookies.get('prevEmotion'), form.current_emotion.data), labels=labels)
        else:
            url = get_random_song()
            resp = make_response(render_template('listen.html', url=url))
            resp.set_cookie('prevEmotion', form.current_emotion.data)
            return resp
'''
@app.route('/finished', methods=('GET', 'POST'))
def finished():
    form = FinishedForm()

    if request.method == 'POST' and form.validate_on_submit():
        return render_template('results.html', data=generate_chart(request.cookies.get('prevEmotion')), labels=labels)

    return render_template('finished.html', form=form)


@app.route('/form', methods=('GET', 'POST'))
def questionnaire():
    form = ContactForm()

    if request.method == 'POST' and form.validate_on_submit():
        url = get_random_song()
        resp = make_response(render_template('listen.html', state='completed', url=url))
        resp.set_cookie('prevEmotion', form.current_emotion.data)
        return resp

        #if state == 'finished':

            #return render_template('results.html', data=generate_chart(request.cookies.get('prevEmotion'), form.current_emotion.data), labels=labels)
        #else:

    return render_template('form.html', form=form)

@app.route('/spotify', methods=('GET', 'POST'))
def spotify():
    
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    oauth = SpotifyOAuth(client_id="ca077b4c1b6b4ea7a33ed0069ec3eecb",
                client_secret="2d2baf7aa1ff4c9792822aefac0ef7e5",
                          redirect_uri="http://127.0.0.1:5000/form/before",
                          state = random_string,
                          scope="user-read-recently-played user-modify-playback-state user-read-private",
                          cache_path=None)
    '''
    token = oauth.get_cached_token()
    print("token: "+token)
    refresh_token = token['refresh_token']
    if oauth.is_token_expired(token):
      oauth.refresh_access_token(refresh_token)
    '''
    return redirect(url_for('questionnaire'))

@app.route('/', methods=('GET', 'POST'))
def index():

    return render_template('index.html')


if __name__ == "__main__":
    app.run()
