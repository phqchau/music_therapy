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

# Create your views here.
SPOTIPY_CLIENT_ID = secrets.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = secrets.SPOTIPY_CLIENT_SECRET
genres = ['afrobeat', 'alt-rock', 'alternative', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'groove', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'ska', 'sleep', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
artists = []
tracks = []

def callback(request):
    return render(request, 'music/spotifyLoginFinish.html',{})

def index(request):
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	redirect_uri = 'http://localhost:8080/music/authUser/'
	context = {'redirect_uri': redirect_uri,}
	return render(request, 'music/index.html', context)

'''def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'music/detail.html', {'question':question})'''

def play(request):
	user_id = "1262880145"
	playlist_id = request.GET.get('playlist_id')
	if not playlist_id:
		playlist_id = "1AE5848cn7V6qHwriTAOZR"
	playlist_uri = "open.spotify.com/user/" + user_id + "/playlist/" + playlist_id
	return render(request, 'music/play.html', {'playlist_uri':playlist_uri})

def authUser(request):
	if request.method == 'GET':
		auth_code = request.GET.get('code')
		if not auth_code:
			redirect_uri = 'http://localhost:8080/music/authUser/'
			context = {'redirect_uri': redirect_uri, 'error_message':'User Authentication failed. Please login again!'}
			return render(request, 'music/index.html', context)

		spotify_url = 'https://accounts.spotify.com/api/token'
		authorization_string = SPOTIPY_CLIENT_ID + ':' + SPOTIPY_CLIENT_SECRET
		redirect_uri = 'http://localhost:8080/music/authUser/'

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

	return HttpResponseRedirect(reverse('music:createPlaylist'))

def createPlaylist(request):
	return render(request, 'music/createPlaylist.html', {'genres': genres, 'artists':artists, 'tracks':tracks})

def chooseArtists(request):
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
	#ArtistSeeds.objects.all().delete()
	for artist_id, artist_name in artists.items():
		request.session['artist'] = (artist_id, artist_name)
		#ArtistSeeds.objects.create(artist_name=artist_name, artist_id=artist_id)
		artist_list.append(artist_name)
	return render(request, 'music/chooseArtists.html', {'artist_list':artist_list})

def processPlaylist(request):
	try:
		pname = request.POST['playlistName']
		artistsFetched = []
		for i in range(1,6):
			artist = request.POST['artists' + str(i)]
			if artist != 'none':
				artistsFetched.append(artist)

	except:
		# Redisplay the question voting form.
		return render(request, 'music/createPlaylist.html', {'genres': genres, 'artists':artists, 'tracks':tracks,'error_message': "You didn't select a choice."})		
	else:
		if request.session.has_key('user_id'):
			user_id = request.session['user_id']
		if request.session.has_key('access_token'):
			access_token = request.session['access_token']
		sp = controller.authenticate_user(access_token)

		if request.session.has_key('genres'):
			genres = request.session['genres']
		if request.session.has_key('age'):
			age = request.session['age']

		#user_id = "1262880145"
		artist_ids = []
		for artist in artistsFetched:
			if request.session.has_key('artist'):
			#artist_id = ArtistSeeds.objects.filter(artist_name=artist).values()[0]['artist_id']
				artist_id = request.session['artist'][0]
				artist_ids.append(artist_id)

		playlist_object = Playlists(playlist_id=playlist_id, user_id=user_id)
		playlist_object.save()

		seedsForPlaylist = SeedsForPlaylist(playlist=playlist_object, playlist_name=pname, age=age, genres=genres, artist_ids=artist_ids)
		seedsForPlaylist.save()

		playlist_id = controller.create_playlist(sp, pname, age, genresFetched, artist_ids)

		playlist_uri = "open.spotify.com/user/" + user_id + "/playlist/" + playlist_id

		#clear the session keeping the seeds info
		if request.session.has_key('genres'): del request.session['genres']
		if request.session.has_key('age'): del request.session['age']
		if request.session.has_key('artist'): del request.session['artist']
		return render(request, 'music/play.html', {'playlist_uri':playlist_uri})
		#return HttpResponse("Playlist has been created!\nYou're looking at {0}".format(new_playlist))
		#return render(request, 'polls/play.html', {'playlist':new_playlist,})
#		return HttpResponseRedirect('polls/play.html?playlist_id={0}'.format(new_playlist))


def viewPlaylist(request):
	return HttpResponse("You're looking at Something new?")
