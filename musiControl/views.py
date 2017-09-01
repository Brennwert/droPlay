from django.shortcuts import render
from django.http import HttpResponse
import Music


music = Music.Music()

def musicPlayer(request):
    return render(request, 'musiControl/musicPlayer.html', {})

def dispatcher(request, action):
    return HttpResponse( getattr(music, action)() )
    #return HttpResponse(action);