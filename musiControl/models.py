from django.db import models

class Album(models.Model):
    dropletID = models.IntegerField()
    type = models.CharField(max_length=10)
    path = models.CharField(max_length=300)
    image = models.CharField(max_length=300)
    playing = models.NullBooleanField()
    
