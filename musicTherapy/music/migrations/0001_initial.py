# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 02:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=60)),
                ('playlist_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SeedsForPlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_name', models.CharField(max_length=60)),
                ('age', models.IntegerField(max_length=3)),
                ('genres', models.CharField(max_length=100)),
                ('artists', models.CharField(max_length=100)),
                ('tracks', models.CharField(max_length=100)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Playlists')),
            ],
        ),
    ]