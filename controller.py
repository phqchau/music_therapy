import sys
import datetime
import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = 'fd766dc7eb804d15b63fc336469a006b'
SPOTIPY_CLIENT_SECRET = '766b527e3783487d93541b0b356b9904'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'
CACHE = '.spotipyoauthcache'

debug = False
>>>>>>> Stashed changes

def show_tracks(tracks):
        for i, item in enumerate(tracks['items']):
                track = item['track']
                print ("   %d %32.32s %s" % (i, track['artists'][0]['name'],
                        track['name']))
			
def authenticate_user(username):
	scope = "playlist-read-private playlist-modify-private playlist-modify-public"
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

        upperLimit = 25

        while len(artists) < 5:
                year_range = get_year_range(age, upperLimit)
                artists += artists_from_year_range_and_genres(sp, year_range, genres)
                upperLimit += 10

        while len(artists) > 5: 
                artists.popitem() 
        artist_ids = artists.keys() 
   
        recommended_tracks = sp.recommendations(seed_genres=genres, seed_artists=artist_ids, limit=30)["tracks"] 

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
        while len(artists) < 5:
                results = sp.search(q='year:' + str(year_range[0]) + '-' + str(year_range[1]), type='album',limit=50)

                albums = results['albums']['items']

                for album in albums:
                        for artist in album['artists']:
                                if artist['id'] not in artists.keys():
                                        artists[artist['id']] = artist['name']
	
                bad_artists = []
			
                for id in artists.keys():
                        current_artist = sp.artist(id)
                        if set(genres).isdisjoint(set(current_artist['genres'])):
                                bad_artists.append(current_artist['id'])
	
                for artist in bad_artists:		
                        del artists[artist]

                year_range[0] -= 10
				year_range[1] += 10
			
	return artists