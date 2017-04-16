# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 01:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_artistseeds'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArtistSeeds',
        ),
        migrations.RenameField(
            model_name='seedsforplaylist',
            old_name='artists',
            new_name='artist_ids',
        ),
        migrations.RemoveField(
            model_name='playlists',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='seedsforplaylist',
            name='tracks',
        ),
    ]
