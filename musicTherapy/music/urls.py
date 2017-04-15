from django.conf.urls import url

from . import views

app_name = 'music'
urlpatterns = [
	# ex: /music/
	url(r'^$', views.index, name='index'),

	# ex: /music/createPlaylist/
	url(r'^createPlaylist/$', views.createPlaylist, name='createPlaylist'),	

	# ex: /music/processPlaylist/
	url(r'^processPlaylist/$', views.processPlaylist, name='processPlaylist'),	

	# ex: /music/viewPlaylist/
	url(r'^viewPlaylist/$', views.viewPlaylist, name='viewPlaylist'),

	url(r'^chooseArtists/$', views.chooseArtists, name='chooseArtists'),	

	# ex: /music/createPlaylist/
	url(r'^play/$', views.play, name='play'),	
]