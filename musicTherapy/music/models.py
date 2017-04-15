import datetime

from django.utils import timezone
from django.db import models

# Create your models here.
class Playlists(models.Model):
	user_id = models.CharField(max_length=50)
	user_name = models.CharField(max_length=60)
	playlist_id = models.CharField(max_length=50)

class SeedsForPlaylist(models.Model):
	playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
	playlist_name = models.CharField(max_length=60)
	age = models.IntegerField(max_length=3)
	genres = models.CharField(max_length=100)
	artists = models.CharField(max_length=100)
	tracks = models.CharField(max_length=100)

class ArtistSeeds(models.Model):
	artist_name = models.CharField(max_length=100)
	artist_id = models.CharField(max_length=100)