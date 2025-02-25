import json
import spotipy 
import webbrowser
import spotipy.util as util
import random as rd

username = 'USERNAME'
clientID = 'CLIENTID'
clientSecret = 'CLIENTSECRET'
redirect_uri = 'http://google.com/callback/'


oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()
sp = __create_spotify_object()
  
# To print the response in readable format.
# print(json.dumps(user_name, sort_keys=True, indent=4))

def __create_spotify_object():
    """Will create a spotify object and return it"""

    # Defining the scope(s) of the application
    scope = "playlist-modify-public playlist-modify-private user-read-currently-playing"

    # Getting the token
    token = util.prompt_for_user_token(username, scope=scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirect_uri)

    # Returning our spotify object
    return spotipy.Spotify(auth=token)

def create_playlist(u,pn): 
    playlists = sp.user_playlists(u)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == pn:  # filter for newly created playlist
            print("This playlist already exists")
            return ""
    sp.user_playlist_create(u, name=pn)

def get_playlist_id(username, playlist_name):
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']
    return playlist_id

def add_tracks_to_playlist(p_id, songs): 
    sp.playlist_add_items(p_id, songs)


def get_track_ids(sample_data):
    track_ids = []
    for i in range(len(sample_data)):
        results = sp.search(q=sample_data[i], limit=5, type='track') #get 5 responses since first isn't always accurate
        if (results['tracks']['total'] == 0): #if track isn't on spotify as queried, go to next track
            continue
        else:
            track_ids.append(results['tracks']['items'][0]['id']) #append track id
    return track_ids


def get_artist_ids(artists):
    artist_ids = []
    for i in range(len(artists)):
        results = sp.search(q=artists[i], limit=5, type='artist') 
        if (results["artists"]['total'] == 0): 
            continue
        else:
            artist_ids.append(results['artists']['items'][0]['uri']) #append artist id
    if(len(artists) != len(artist_ids)): print('not all artists on spotify')
    return artist_ids

def find_artist_songs(artist_id):
    alb_list = sp.artist_albums(artist_id, 'album', limit=50)
    alb_ids = []
    for i in range(len(alb_list['items'])):
        alb_ids.append(alb_list['items'][i]['id'])
    song_id_list = []
    for j in alb_ids:
        for k in sp.album_tracks(j)['items']:
            song_id_list.append(k['uri'])
    return song_id_list

def show_artist_albums(artist_id):
    albums = []
    results = sp.artist_albums(artist_id, album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_album_tracks(albums):
    tracks = []
    for i in range(len(albums)):
        results = sp.album_tracks(albums[i]['id'])
        tracks.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
    return tracks


def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    return albums

def feature_finder(artist):
    songs = all_songs(artist)
    artist_name_list = []
    for i in range(len(songs)):
        for j in range(len(songs[i]['artists'])):
            artist_name_list.append(songs[i]['artists'][j]['name'])
    return list(set(artist_name_list))


def all_songs(artist1):
    artist = get_artist(artist1)
    albums = show_artist_albums(artist)
    return show_album_tracks(albums)



# **********
#outputs every artist that the given artist has worked with on spotify songs
if __name__ == "__main__":
  print(feature_finder(input("Which artist's features would you like to see?: ").strip()))
