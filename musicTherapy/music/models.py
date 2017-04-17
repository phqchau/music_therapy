import datetime

from django.utils import timezone
from django.db import models

# store a user's playlists, associating each playlist id with the user id of its creator
class Playlists(models.Model):
	playlist_id = models.CharField(max_length=50)
	user_id = models.CharField(max_length=50)

# store user inputs for use in playlist creation and potentially in additional features added later
# each entry is associated with a specified playlist
class SeedsForPlaylist(models.Model):
	playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
	playlist_name = models.CharField(max_length=60)
	age = models.IntegerField(max_length=3)
	genres = models.CharField(max_length=100)
	artist_ids = models.CharField(max_length=100)