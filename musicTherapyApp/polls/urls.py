from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
	# ex: /polls/
	url(r'^$', views.index, name='index'),

	# ex: /polls/5/
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),

	# ex: /polls/5/results/
	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),

	# ex: /polls/5/vote/
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),	

	# ex: /polls/createPlaylist/
	url(r'^createPlaylist/$', views.createPlaylist, name='createPlaylist'),	

	# ex: /polls/processPlaylist/
	url(r'^processPlaylist/$', views.processPlaylist, name='processPlaylist'),	

	# ex: /polls/viewPlaylist/
	url(r'^viewPlaylist/$', views.viewPlaylist, name='viewPlaylist'),	

	# ex: /polls/createPlaylist/
	url(r'^play/$', views.play, name='play'),	
]