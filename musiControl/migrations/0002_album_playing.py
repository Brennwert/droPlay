# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-25 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiControl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='playing',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
