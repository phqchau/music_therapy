import sys
import datetime
import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = 'fd766dc7eb804d15b63fc336469a006b'
SPOTIPY_CLIENT_SECRET = '766b527e3783487d93541b0b356b9904'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'
CACHE = '.spotipyoauthcache'

<<<<<<< HEAD
SPOTIPY_CLIENT_ID = '52451274c0ed4367af773d2d957f5566'
SPOTIPY_CLIENT_SECRET = 'ce14846193dc4a7384e0bd411b93debb'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback/'
CACHE = '.spotipyauthcache'
=======
debug = False
>>>>>>> Stashed changes
>>>>>>> cea4d9cd6c5415b6961be3fcbc947884d72dbfdb

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

        year_range = get_year_range(age)
 
        artists = artists_from_year_range_and_genres(sp, year_range, genres) 
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
	
def artists_from_year_range_and_genres(sp, range, genres):
	results = sp.search(q='year:' + str(range[0]) + '-' + str(range[1]), type='album',limit=50)

	albums = results['albums']['items']

	artists = {}
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
<<<<<<< HEAD
	print(artists)
		
=======
			
>>>>>>> cea4d9cd6c5415b6961be3fcbc947884d72dbfdb
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

def downvote(sp, track_id, playlist_id, genre_id, username):

        sp.display_playlist_tracks(sp, playlist_id)

        for i in sp.audio_features(track_id):
                danceability = i["danceability"]
                energy = i["energy"]
                mode = i["mode"]
                speechiness = i["speechiness"]
                acousticness = i["acousticness"]
                instrumentalness = i["instrumentalness"]
                liveness = i["liveness"]
                valence = i["valence"]
                tempo = i["tempo"]

                danceability = 1 - danceability
                energy = 1 - energy
                mode = 1 - mode
                speechiness = 1 - speechiness
                acousticness = 1 - acousticness
                instrumentalness = 1 - instrumentalness
                liveness = 1 - liveness
                valence = 1 - valence

        if tempo >= 114:
                i = 0
                tempoLimit = 114
                results = sp.recommendations(seed_genres = genre_id, limit = 100, max_tempo = tempoLimit,
                                             target_danceability = danceability, target_energy = energy,
                                             target_mode = mode, target_speechiness = speechiness,
                                             target_acousticness = acousticness, target_instrumentalness = instrumentalness,
                                             target_liveness = liveness, target_valence = valence)["tracks"]
                for track in results:
                        if i == 5:
                                break
                        else:
                                addTrack = {track["id"]}
                                sp.user_playlist_add_tracks(username, playlist_id, addTrack)
                        i += 1
        else:
                i = 0
                tempoLimit = 114
                results = sp.recommendations(seed_genres = genre_id, limit = 100, max_tempo = tempoLimit,
                                             target_danceability = danceability, target_energy = energy,
                                             target_mode = mode, target_speechiness = speechiness,
                                             target_acousticness = acousticness, target_instrumentalness = instrumentalness,
                                             target_liveness = liveness, target_valence = valence)["tracks"]
                for track in results:
                        if i ==5:
                                break
                        else:
                                addTrack = {track["id"]}
                                sp.user_playlist_add_tracks(username, playlist_id, addTrack)
                        i += 1

        removeTrack = {track_id}
        sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, removeTrack)

        display_playlist_tracks(sp, playlist_id)
	
if __name__ == '__main__':
	sp = authenticate_user("fcurrin")
	user_id = sp.current_user()["id"]

	new_playlist = create_playlist(sp, "test_artists_90", 90, ["jazz", "big band", "classical"])
    
	display_playlist_tracks(sp, new_playlist)
	
	#artists_from_year_range_and_genres(sp, get_year_range(90), ["jazz", "big band", "classical"])
