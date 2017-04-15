import datetime

from django.utils import timezone
from django.db import models
#from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

"""class Playlists(models.Model):
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
"""
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text	
