from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse

import music.controller as controller
import music.secrets as secrets
from music.models import Playlists, SeedsForPlaylist
import base64
import requests
import json
import ast

SPOTIPY_CLIENT_ID = secrets.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = secrets.SPOTIPY_CLIENT_SECRET
genres = ['afrobeat', 'alt-rock', 'alternative', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'groove', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'ska', 'sleep', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
artists = []
tracks = []

def index(request):
	redirect_uri = 'http://musictherapy.pythonanywhere.com/music/authUser/'
	context = {'redirect_uri': redirect_uri,}
	return render(request, 'music/index.html', context)

def about(request):
	context = {}
	return render(request, 'music/about.html', context)

def play(request, playlist_id):
	if request.session.has_key('user_id'):
		user_id = request.session['user_id']
	if not playlist_id:
		playlist_id = "1AE5848cn7V6qHwriTAOZR"
	playlist_uri = "open.spotify.com/user/" + user_id + "/playlist/" + playlist_id
	return render(request, 'music/play.html', {'playlist_uri':playlist_uri})

def authUser(request):
	if request.method == 'GET':
		auth_code = request.GET.get('code')
		if not auth_code:
			redirect_uri = 'http://musictherapy.pythonanywhere.com/music/authUser/'
			context = {'redirect_uri': redirect_uri, 'error_message':'User Authentication failed. Please login again!'}
			return render(request, 'music/index.html', context)

		spotify_url = 'https://accounts.spotify.com/api/token'
		authorization_string = SPOTIPY_CLIENT_ID + ':' + SPOTIPY_CLIENT_SECRET
		redirect_uri = 'http://musictherapy.pythonanywhere.com/music/authUser/'

		headers = {
			'Authorization' : 'Basic ' + base64.b64encode(bytes(authorization_string, "utf-8")).decode("ascii")
		} 
		post_data = {
			'code': auth_code,
			'redirect_uri': redirect_uri,
			'grant_type': 'authorization_code',
		}

	response = requests.post(spotify_url, data=post_data, headers=headers)
	content = response.content.decode("utf-8")
	access_token = ast.literal_eval(content)['access_token']

	request.session['access_token'] = access_token

	return HttpResponseRedirect(reverse('music:getUserInfo'))

def getUserInfo(request):
	if request.session.has_key('access_token'):
		access_token = request.session['access_token']	

	new_header = {
		'Authorization' : 'Bearer ' + access_token
	}

	get_data_url = "https://api.spotify.com/v1/me"
	response_new = requests.get(get_data_url, headers=new_header)
	content_new = response_new.content.decode("utf-8")
	user_id = json.loads(content_new)['id']

	request.session['user_id'] = user_id

	return HttpResponseRedirect(reverse('music:viewPlaylist'))

def createPlaylist(request):
	return render(request, 'music/createPlaylist.html', {'genres': genres, 'artists':artists, 'tracks':tracks})

def chooseArtists(request):
	try:
		if request.session.has_key('access_token'):
			access_token = request.session['access_token']
		sp = controller.authenticate_user(access_token)
		genresFetched = []
		for i in range(1,6):
			genre = request.POST['genres' + str(i)]
			if genre != 'none':
				genresFetched.append(genre)
		request.session['genres'] = genresFetched

		age = request.POST['age']
		if age:
			age = int(age)
		request.session['age'] = age
		artists = controller.artists_from_year_range_and_genres(sp, genresFetched, age)
		artist_list = []
		artist_id_list = []

		for artist_id, artist_name in artists.items():
			artist_list.append(artist_name)
			artist_id_list.append(tuple((artist_id, artist_name)))

		sorted_artist_list = sorted(artist_list)
		request.session['artist'] = artist_id_list
	except:
		return render(request, 'music/createPlaylist.html', {'genres': genres, 'error_message': "Oops, either you didn't provide enough information or your search didn't return any artist. Please try a different search."})
	return render(request, 'music/chooseArtists.html', {'artist_list':sorted_artist_list})

def processPlaylist(request):
	try:
		pname = request.POST['playlistName']
		artistsFetched = []
		for i in range(1,6):
			artist = request.POST['artists' + str(i)]
			if artist != 'none':
				artistsFetched.append(artist)
	except:
		if request.session.has_key('artist'):
			sorted_artist_list = request.session['artist']
		return render(request, 'music/chooseArtists.html', {'artist_list':sorted_artist_list,'error_message': "You didn't provide a playlist name or pick any artist."})

	if request.session.has_key('user_id'):
		user_id = request.session['user_id']
	if request.session.has_key('access_token'):
		access_token = request.session['access_token']
	sp = controller.authenticate_user(access_token)

	if request.session.has_key('genres'):
		genres = request.session['genres']
	if request.session.has_key('age'):
		age = request.session['age']

	artist_ids = []
	for artist in artistsFetched:
		if request.session.has_key('artist'):
			for artist_id_name in request.session['artist']:
				if artist_id_name[1] == artist:
					artist_ids.append(artist_id_name[0])

	playlist_id = controller.create_playlist(sp, pname, age, genres, artist_ids)

	playlist_object = Playlists(playlist_id=playlist_id, user_id=user_id)
	playlist_object.save()

	seedsForPlaylist = SeedsForPlaylist(playlist=playlist_object, playlist_name=pname, age=age, genres=genres, artist_ids=artist_ids)
	seedsForPlaylist.save()

	playlist_uri = "open.spotify.com/user/" + user_id + "/playlist/" + playlist_id

	return render(request, 'music/play.html', {'playlist_uri':playlist_uri})

def viewPlaylist(request):
	if request.session.has_key('user_id'):
		user_id = request.session['user_id']
	list_of_playlists = Playlists.objects.filter(user_id=user_id)
	list_of_playlist_tuples = []
	for playlist in list_of_playlists:
		Seeds = SeedsForPlaylist.objects.get(playlist=playlist)
		playlist_id = playlist.playlist_id
		playlist_name = Seeds.playlist_name
		list_of_playlist_tuples.append((playlist_name,playlist_id))

	#clear the session keeping the seeds info
	if request.session.has_key('genres'): del request.session['genres']
	if request.session.has_key('age'): del request.session['age']
	if request.session.has_key('artist'): del request.session['artist']

	return render(request, 'music/viewPlaylist.html', {'list_of_playlist_tuples':list_of_playlist_tuples})		
