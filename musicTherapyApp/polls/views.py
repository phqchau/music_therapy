from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse

from .models import Question
import polls.controller as controller

# Create your views here.
genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
artists = []
tracks = []

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list':latest_question_list,}
	#output = ', '.join([q.question for q in latest_question_list])
	return render(request, 'polls/index.html', context)
	#return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question':question})

def play(request):
	user_name = "Chau&nbsp;Pham"
	playlist_id = request.GET.get('playlist_id')
	if not playlist_id:
		playlist_id = "1AE5848cn7V6qHwriTAOZR"
	playlist_uri = "spotify:user:" + user_name + ":playlist:" + playlist_id
	return render(request, 'polls/play.html', {'playlist_uri':playlist_uri})

def createPlaylist(request):
	return render(request, 'polls/createPlaylist.html', {'genres': genres, 'artists':artists, 'tracks':tracks})

def processPlaylist(request):
	try:
		pname = request.POST["playlistName"]
		age = request.POST["age"]
		if age:
			age = eval(age)
		genresFetched = request.POST.getlist("genres")
	except:
		# Redisplay the question voting form.
		return render(request, 'polls/createPlaylist.html', {'genres': genres, 'artists':artists, 'tracks':tracks,'error_message': "You didn't select a choice."})		
	else:
		sp = controller.authenticate_user("Chau&nbsp;Pham")
		new_playlist = controller.create_playlist(sp, pname, age, genresFetched)
		user_name = "Chau&nbsp;Pham"
		playlist_uri = "spotify:user:" + user_name + ":playlist:" + new_playlist
		return render(request, 'polls/play.html', {'playlist_uri':playlist_uri})
		#request.session
		#return HttpResponse("Playlist has been created!\nYou're looking at {0}".format(new_playlist))
		#return render(request, 'polls/play.html', {'playlist':new_playlist,})
#		return HttpResponseRedirect('polls/play.html?playlist_id={0}'.format(new_playlist))


def viewPlaylist(request):
	return HttpResponse("You're looking at Something new?")

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		# Always return an HttpResponseRedirect after successfully dealing with POST data.
		# This prevents data from being posted twice if a user hits the Back button

		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
