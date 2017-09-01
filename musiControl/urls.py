from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^$', views.musicPlayer, name='musicPlayer'),
            url(r'^music/(?P<action>.*)$', views.dispatcher, name='dispatcher'),
            ]
