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

	# ex: /music/authUser/
	url(r'^authUser/$', views.authUser, name='authUser'),	

	# ex: /music/getUserInfo/
	url(r'^getUserInfo/$', views.getUserInfo, name='getUserInfo'),	

	# ex: /music/viewPlaylist/
	url(r'^viewPlaylist/$', views.viewPlaylist, name='viewPlaylist'),

	# ex: /music/chooseArtists/
	url(r'^chooseArtists/$', views.chooseArtists, name='chooseArtists'),	

	# ex: /music/play/
	url(r'^(?P<playlist_id>[0-9a-zA-Z]+)/play/$', views.play, name='play'),	
]