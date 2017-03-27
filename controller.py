import sys
import spotipy
import spotipy.util as util

def show_tracks(tracks):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		print ("   %d %32.32s %s" % (i, track['artists'][0]['name'],
			track['name']))
			
def authenticate_user(username):
	scope = "playlist-read-private playlist-modify-private"
	token = util.prompt_for_user_token(username, scope)
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
	
	
if __name__ == '__main__':
	sp = authenticate_user("fcurrin")
	#display_playlists(sp)
	#print(sp.recommendation_genre_seeds())
	new_playlist = create_playlist(sp, "01test", genres=["classical", "opera", "happy"])
	display_playlist_tracks(sp, new_playlist)