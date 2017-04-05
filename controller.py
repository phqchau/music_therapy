import sys
import datetime
import spotipy
import spotipy.util as util


SPOTIPY_CLIENT_ID = 'e080565ae7b6446586dc8431f57358a6'
SPOTIPY_CLIENT_SECRET = 'secret goes here ;)'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

debug = False

def show_tracks(tracks):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		print ("   %d %32.32s %s" % (i, track['artists'][0]['name'],
			track['name']))
			
def authenticate_user(username):
	scope = "playlist-read-private playlist-modify-private"
	token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
	sp = spotipy.Spotify(auth=token)
	return sp
	
def display_playlists(sp):
	playlists = sp.current_user_playlists()
	print("Playlists:")
	for playlist in playlists["items"]:
		print(playlist["name"])
		
def create_playlist(sp, name, artists=None, genres=None, tracks=None):
	userID = sp.current_user()["id"]
	playlist = sp.user_playlist_create(userID, name, public=False)
	playlist_id = playlist["id"]
	recommended_tracks = sp.recommendations(artists, genres, tracks)
	track_uris = []
	for track in recommended_tracks["tracks"]:
		track_uris.append(track["uri"])
	sp.user_playlist_add_tracks(userID, playlist_id, track_uris)
	return playlist_id
	
def display_playlist_tracks(sp, playlist_id):
	userID = sp.current_user()["id"]
	results = sp.user_playlist(userID, playlist_id, fields="tracks,next")
	tracks = results["tracks"]
	show_tracks(tracks)
	while tracks["next"]:
		tracks = sp.next(tracks)
		show_tracks(tracks)

# returns min: the year the user was 15, and max: the year the user was 25		
def get_year_range(age):
	current_year = datetime.datetime.today().year
	min = current_year - age + 15
	max = current_year - age + 25
	return min, max
	
def albums_from_year_range(sp, range):
	results = sp.search(q='year:' + str(range[0]) + '-' + str(range[1]), type='album',limit=10)
	print(results)
	albums = results['albums']['items']
	#while results['next']:
	#	albums.extend(results['items'])

	for album in albums:
		print(album['name'])
		for artist in album['artists']:
			print(artist['name'])
	
def albums_from_year_range_and_genre(sp, range, genre):
	results = sp.search(q='year:' + str(range[0]) + '-' + str(range[1]), type='album',limit=50)
	#print(results)

	if debug:
		print(results)
	albums = results['albums']['items']

	artists = {}
	for album in albums:
		if debug:
			print(album['name'])
		for artist in album['artists']:
			if artist['name'] not in artists:
				if debug:
					print(artist['name'])
				artists[artist['name']] = artist['id']
	if debug:
		print(artists)
	
	bad_artists = []
			
	for artist in artists:
		current_artist = sp.artist(artists[artist])
		if debug:
			print(current_artist['genres'])
		if genre not in current_artist['genres']:
			bad_artists.append(artist)
	
	for artist in bad_artists:		
		del artists[artist]
			
	print(artists)

			
'''			
fetch 50 albums from time period
pull list of artists from albums (no various artists)
for each artist:
	for each genre:
		check if it's one of the approved ones, if so put artist in new list
use genre, random 4 artists from new list for recommendation seeds
'''			
	
if __name__ == '__main__':
	sp = authenticate_user("il3eli")
	#debug = True
	#display_playlists(sp)
	#print(sp.recommendation_genre_seeds())
	#new_playlist = create_playlist(sp, "01test", genres=["classical", "opera", "happy"])
	#display_playlist_tracks(sp, new_playlist)
	range = get_year_range(90)
	print('jazz artists for ' + str(range))
	albums_from_year_range_and_genre(sp, range, 'jazz')
	print('big band artists for ' + str(range))
	albums_from_year_range_and_genre(sp, range, 'big band')
	print('classical artists for ' + str(range))
	albums_from_year_range_and_genre(sp, range, 'classical')
	
	range = get_year_range(75)
	print('jazz artists for ' + str(range))
	albums_from_year_range_and_genre(sp, range, 'jazz')
	print('big band artists for ' + str(range))
	albums_from_year_range_and_genre(sp, range, 'big band')
	print('classical artists for ' + str(range))
	albums_from_year_range_and_genre(sp, range, 'classical')
