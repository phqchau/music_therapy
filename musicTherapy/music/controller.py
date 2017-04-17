import sys
import datetime
import spotipy
import spotipy.util as util
import music.secrets as secrets
			
'''
authenticate the user given an access token, access private playlists and gain ability to modify them
create a Spotify object used to call all the necessary Spotipy functions in later portions of code
'''
def authenticate_user(token):
	scope = "playlist-read-private playlist-modify-private"
	sp = spotipy.Spotify(auth=token)
	return sp
		
'''
uses Spotipy's recommendations function to generate up to 30 tracks using the user's selected genres and artists
creates a playlist and adds those tracks to the playlist
returns the playlist id so it can be recorded as one of the user's created playlists and accessed later
'''
def create_playlist(sp, name, age, genres, artist_ids):
	user_id = sp.current_user()["id"]

	year_range = get_year_range(age)
	
	recommended_tracks = sp.recommendations(seed_genres=genres, seed_artists=artist_ids, limit=30)["tracks"]

	track_uris = []
	for track in recommended_tracks:
		track_uris.append(track["uri"])
	
	playlist = sp.user_playlist_create(user_id, name, public=False)
	playlist_id = playlist["id"]
	sp.user_playlist_add_tracks(user_id, playlist_id, track_uris)
	
	return playlist_id

'''
return min: the year the user was 15, and max: the year the user was 25
called by artists_from_year-range_and_genres
'''	
def get_year_range(age):
	current_year = datetime.datetime.today().year
	min = current_year - age + 15
	max = current_year - age + 25
	return [min, max]
	
'''			
uses a Spotify search query to find up to 20 artists per genre in the given year range
if fewer than 5 artists produced from this search, uses genres without year ranges
returns dictionary of artist ids mapped to artist names, users select up to 5 names, and
the associated ids are given to create_playlist
'''		
def artists_from_year_range_and_genres(sp, genres, age):
		artists = {}
		year_range = get_year_range(age)
		for genre in genres:
			try:
				results = sp.search(q='year:' + str(year_range[0]) + '-' + str(year_range[1]) + ' genre:' + genre, type='artist',limit=20)
				for artist in results['artists']['items']:
					if artist['id'] not in artists.keys():
						artists[artist['id']] = artist['name']
			except:
				continue

		if len(artists) < 5:
			for genre in genres:
				results = sp.search(q='genre:' + genre, type='album',limit=20)
				for artist in results['artists']['items']:
					if artist['id'] not in artists.keys():
						artists[artist['id']] = artist['name']
		
		return artists

'''
functions below were used primarily for testing purposes
'''		
def show_tracks(tracks):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		print ("   %d %32.32s %s" % (i, track['artists'][0]['name'],
			track['name']))
			
def display_playlists(sp):
	playlists = sp.current_user_playlists()
	print("Playlists:")
	for playlist in playlists["items"]:
		print(playlist["name"])
		
def display_playlist_tracks(sp, playlist_id):
	userID = sp.current_user()["id"]
	results = sp.user_playlist(userID, playlist_id, fields="tracks,next")
	tracks = results["tracks"]
	show_tracks(tracks)
	while tracks["next"]:
		tracks = sp.next(tracks)
		show_tracks(tracks)