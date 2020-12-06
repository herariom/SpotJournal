import spotipy, random, json, requests, string
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import SearchVideos

from song_data import SongData
from sql import SpotSQL

current_song = ""
current_user_id = ""

def get_spotipy_objs():
  # Returns two list array with ouath and sp object
  letters = string.ascii_lowercase
  random_string = ''.join(random.choice(letters) for i in range(10))
  oauth = SpotifyOAuth(client_id="ca077b4c1b6b4ea7a33ed0069ec3eecb",
                      client_secret="2d2baf7aa1ff4c9792822aefac0ef7e5",
                      redirect_uri="https://favorable-mark-297715.uc.r.appspot.com/form/",
                      state = random_string,
                      scope="user-read-recently-played user-modify-playback-state user-read-private",
                      cache_path=None)
  token_dict = oauth.get_cached_token()
  token = token_dict['access_token']
  refresh_token = token_dict['refresh_token']
  if oauth.is_token_expired(token_dict):
    oauth.refresh_access_token(refresh_token)
  sp = spotipy.Spotify(auth_manager=oauth)
  current_user_id = sp.current_user()['id']
  return [oauth, sp]

def get_random_song(past_songs = []):
  # past_songs: parameter list that contains names of all songs already chosen for user before
  db = SpotSQL()
  [oauth, sp] = get_spotipy_objs()
  results = sp.current_user_recently_played(limit=50) # Dictionary of user's recently played tracks (@https://developer.spotify.com/console/get-recently-played/)
  user_id = sp.current_user()['id']

  # Random song selection
  all_tracks = [] # Stores list of 50 recently played tracks 
  for item in results['items']:
      track = item['track']
      #all_tracks.append(track['name']+ ' - ' +track['artists'][0]['name'])
      all_tracks.append(track['name'])
  random_song = random.choice(all_tracks)
  while random_song in past_songs:
    random_song = random.choice(all_tracks)

  current_song = random_song  
  db.add_song(random_song)  # add song to database
  random_song += " music video"
  yt_embed_link = findYTLink(random_song)
  db.connection.close()
  return yt_embed_link

def get_song_name():
  return current_song

def get_user_id(): 
  # Returns user's unique Spotify ID
  #[oauth, sp] = get_spotipy_objs()
  #results = sp.current_user_recently_played(limit=50) # Dictionary of user's recently played tracks (@https://developer.spotify.com/console/get-recently-played/)
  #user_id = sp.current_user()['id'] 
  return current_user_id

def findYTLink(search):
    # Function returns a YouTube ID/Link of the random_song in String datatype.
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

def spotify():
    db = SpotSQL()
    [oauth, sp] = get_spotipy_objs()
    user_id = sp.current_user()['id'] # Unique ID of Spotify User
    db.add_user(user_id)
    db.connect.close()