# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-25 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dropletID', models.IntegerField()),
                ('type', models.CharField(max_length=10)),
                ('path', models.CharField(max_length=300)),
                ('image', models.CharField(max_length=300)),
            ],
        ),
    ]