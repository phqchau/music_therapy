import sys
import datetime
import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = "fd766dc7eb804d15b63fc336469a006b"
SPOTIPY_CLIENT_SECRET = "766b527e3783487d93541b0b356b9904"
SPOTIPY_REDIRECT_URI = "http://localhost:8080/callback"
CACHE = '.spotipyoauthcache'

debug = False

def authenticate_user(username):
    scope = "playlist-read-private playlist-modify-private playlist-modify-public"
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    return sp

def dislike(sp, track_id, playlist_id, genre_id, username):

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
        
if __name__ == "__main__":
    username = "22nisbf24xx7ftl6zemmjnncy"
    sp = authenticate_user(username)
    track_id = "6NaRzSvVxqv2DC2eg039gB"
    playlist_id = "2D4mUa3PxWTZmQXV9vjgIq"
    genre_id = ["pop"]
    dislike(sp, track_id, playlist_id, genre_id, username)