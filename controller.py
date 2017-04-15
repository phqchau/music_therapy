import sys
import datetime
import spotipy
import spotipy.util as util


SPOTIPY_CLIENT_ID = '9da0c8416b0e429a858497713be2b92a'
SPOTIPY_CLIENT_SECRET = 'a73170daa78142a1a22371cbe7c9f8f2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-read-private playlist-modify-private'
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
		
def create_playlist(sp, name, age, genres, artists=None, tracks=None):
	user_id = sp.current_user()["id"]
	playlist = sp.user_playlist_create(user_id, name, public=False)
	playlist_id = playlist["id"]
	
	year_range = get_year_range(age)
	
	if artists:
		artists = artists + artists_from_year_range_and_genres(sp, year_range, genres)
	else:
		artists = artists_from_year_range_and_genres(sp, year_range, genres)
	
	recommended_tracks = []
	i = 0
	if len(artists) > 0:
		while(i + 5 < len(artists)):
			recommended_tracks += sp.recommendations(seed_artists=artists[i:i+5], limit=10)["tracks"]
			i += 5
		recommended_tracks += sp.recommendations(seed_artists=artists[i:], limit=10)["tracks"]
	recommended_tracks = sp.recommendations(seed_genres = genres, seed_tracks = tracks, limit=30)["tracks"]
	track_uris = []
	for track in recommended_tracks:
		track_uris.append(track["uri"])
	sp.user_playlist_add_tracks(user_id, playlist_id, track_uris)
	
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
	
def artists_from_year_range_and_genres(sp, range, genres):
	results = sp.search(q='year:' + str(range[0]) + '-' + str(range[1]), type='album',limit=50)
	#print(results)

	if debug:
		print(results)
	albums = results['albums']['items']

	artists = []
	for album in albums:
		if debug:
			print(album['name'])
		for artist in album['artists']:
			if artist['id'] not in artists:
				if debug:
					print(artist['name'])
				artists.append(artist['id'])
	if debug:
		print(artists)
	
	bad_artists = []
			
	for id in artists:
		current_artist = sp.artist(id)
		if debug:
			print(current_artist['genres'])
		if set(genres).isdisjoint(set(current_artist['genres'])):
			bad_artists.append(current_artist['id'])
	
	for artist in bad_artists:		
		artists.remove(artist)
			
	return artists

			
'''			
fetch 50 albums from time period
pull list of artists from albums (no various artists)
for each artist:
	for each genre:
		check if it's one of the approved ones, if so put artist in new list
use genre, random 4 artists from new list for recommendation seeds
'''		

def upvote(sp, playlist_id, track):
	user_id = sp.current_user()["id"]
	
	recommended_tracks = sp.recommendations(seed_tracks=[track], limit=5)["tracks"]	
	track_uris = []
	for track in recommended_tracks:
		track_uris.append(track["uri"])
	sp.user_playlist_add_tracks(user_id, playlist_id, track_uris)
	
if __name__ == '__main__':
	sp = authenticate_user("fcurrin")
	user_id = sp.current_user()["id"]
	#debug = True
	#display_playlists(sp)
	file = open("genres", "w")
	file.write(str(sp.recommendation_genre_seeds()))
	file.close()
	
	#new_playlist = create_playlist(sp, "test_artists_90", 90, ["jazz", "big band", "classical"])
	#display_playlist_tracks(sp, new_playlist)
	
	#new_playlist = create_playlist(sp, "test_artists_75", 75, ["jazz", "big band", "classical"])
	#display_playlist_tracks(sp, new_playlist)
