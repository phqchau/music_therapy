import sys
import datetime
import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = "fd766dc7eb804d15b63fc336469a006b"
SPOTIPY_CLIENT_SECRET = "766b527e3783487d93541b0b356b9904"
SPOTIPY_REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = 'playlist-read-private playlist-modify-private'
CACHE = '.spotipyoauthcache'

debug = False

def authenticate_user(username):
    scope = "playlist-read-private playlist-modify-private"
    token = util.prompt_for_user_token(username, scope,
                                       client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET,
                                       redirect_uri=SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    return sp

def dislike(sp, track_id, playlist_id, username):
    #sp.user_playlist_remove_all_occruences_of_tracks(username, playlist_id, track_id)

    for i in sp.audio_features(track_id):
        dance = i["danceability"]
        energyPower = i["energy"]
        modality = i["mode"]
        speech = i["speechiness"]
        acoustic = i["acousticness"]
        instrumental = i["instrumentalness"]
        live = i["liveness"]
        valenceness = i["valence"]
        tempos = i["tempo"]

    dance = 1 - dance
    energyPower = 1 - energyPower
    modality = 1 - modality
    speech = 1 - speech
    acoustic = 1 - acoustic
    instrumental = 1 - instrumental
    live = 1 - live
    valenceness = 1 - valenceness

    rec = sp.recommendations(limit = 5, country = None, target_danceability = dance)
    for track in rec["tracks"]:
        print(track)

    """
     if tempo >= 114:
             tempo = 
     else:
             tempo =
    """
     
     
    
if __name__ == "__main__":
    username = "Abraham Oh"
    sp = authenticate_user(username)
    track_id = "6rqhFgbbKwnb9MLmUQDhG6"
    playlist_id = ""
    dislike(sp, track_id, playlist_id, username)
