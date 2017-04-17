import sys
import datetime
import spotipy
import spotipy.util as util
import music.secrets as secrets

def show_tracks(tracks):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		print ("   %d %32.32s %s" % (i, track['artists'][0]['name'],
			track['name']))
			
def authenticate_user(token):
	scope = "playlist-read-private playlist-modify-private"
	sp = spotipy.Spotify(auth=token)
	return sp

	
def display_playlists(sp):
	playlists = sp.current_user_playlists()
	print("Playlists:")
	for playlist in playlists["items"]:
		print(playlist["name"])
		
def create_playlist(sp, name, age, genres, artist_ids):
	user_id = sp.current_user()["id"]

	year_range = get_year_range(age)
	
	recommended_tracks = sp.recommendations(seed_artists=artist_ids, limit=30)["tracks"]

	track_uris = []
	for track in recommended_tracks:
		track_uris.append(track["uri"])
	
	playlist = sp.user_playlist_create(user_id, name, public=False)
	playlist_id = playlist["id"]
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
	return [min, max]
	
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
	
'''			
fetch 50 albums from time period
pull list of artists from albums (no various artists)
for each artist:
	for each genre:
		check if it's one of the approved ones, if so put artist in new list
use genre, random 4 artists from new list for recommendation seeds
'''		
def artists_from_year_range_and_genres(sp, genres, age):
		artists = {}
		year_range = get_year_range(age)
		for genre in genres:
			try:
				results = sp.search(q='year:' + str(year_range[0]) + '-' + str(year_range[1]) + ' genre:' + genre, type='artist',limit=50)
				for artist in results['artists']['items']:
					if artist['id'] not in artists.keys():
						artists[artist['id']] = artist['name']
			except:
				continue

		if len(artists) < 5:
			for genre in genres:
				results = sp.search(q='genre:' + genre, type='album',limit=50)
				for artist in results['artists']['items']:
					if artist['id'] not in artists.keys():
						artists[artist['id']] = artist['name']
		return artists