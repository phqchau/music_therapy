from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse

import music.controller as controller
from music.models import Playlists, SeedsForPlaylist

# Create your views here.
genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
artists = []
tracks = []

def callback(request):
    return render(request, 'music/spotifyLoginFinish.html',{})

def index(request):
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	return render(request, 'music/index.html', {})

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

def createPlaylist(request):
	return render(request, 'music/createPlaylist.html', {'genres': genres, 'artists':artists, 'tracks':tracks})

def chooseArtists(request):
	sp = controller.authenticate_user("Chau&nbsp;Pham")
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
	year_range = controller.get_year_range(age)
	artists = controller.artists_from_year_range_and_genres(sp, year_range, genresFetched)
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
		sp = controller.authenticate_user("Chau&nbsp;Pham")

		#new_playlist = controller.create_playlist(sp, pname, age, genresFetched)
		if request.session.has_key('genres'):
			genres = request.session['genres']
		if request.session.has_key('age'):
			age = request.session['age']

		user_id = "1262880145"
		artist_ids = []
		for artist in artistsFetched:
			if request.session.has_key('artist'):
			#artist_id = ArtistSeeds.objects.filter(artist_name=artist).values()[0]['artist_id']
				artist_id = request.session['artist'][0]
				artist_ids.append(artist_id)

		recommended_tracks = sp.recommendations(seed_genres=genres, seed_artists=artist_ids, limit=30)['tracks']

		track_uris = []
		for track in recommended_tracks:
			track_uris.append(track["uri"])
		
		playlist = sp.user_playlist_create(user_id, pname, public=False)
		playlist_id = playlist["id"]

		playlist_object = Playlists(playlist_id=playlist_id, user_id=user_id)
		playlist_object.save()

		seedsForPlaylist = SeedsForPlaylist(playlist=playlist_object, playlist_name=pname, age=age, genres=genres, artist_ids=artist_ids)
		seedsForPlaylist.save()

		sp.user_playlist_add_tracks(user_id, playlist_id, track_uris)

		playlist_uri = "open.spotify.com/user/" + user_id + "/playlist/" + playlist_id

		#clear the session keeping the seeds info
		del request.session['genres']
		del request.session['age']
		del request.session['artist']
		return render(request, 'music/play.html', {'playlist_uri':playlist_uri})
		#return HttpResponse("Playlist has been created!\nYou're looking at {0}".format(new_playlist))
		#return render(request, 'polls/play.html', {'playlist':new_playlist,})
#		return HttpResponseRedirect('polls/play.html?playlist_id={0}'.format(new_playlist))


def viewPlaylist(request):
	return HttpResponse("You're looking at Something new?")

'''def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'music/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'music/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		# Always return an HttpResponseRedirect after successfully dealing with POST data.
		# This prevents data from being posted twice if a user hits the Back button

		return HttpResponseRedirect(reverse('music:results', args=(question.id,)))'''