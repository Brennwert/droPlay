import os
import subprocess
#from musiControl.models import Album

class Music:

	def __init__(self):
		os.system("mocp -P")
		self.state = 'pause'

	def play(self, obj = None):
		self.state = 'play'

		if obj:
			self.path = obj.path
			#Album.objects.filter(path=obj.path).playing = True
			
			fullpath = self.root + obj.path
			print("Playing " + fullpath)

			if obj.type == 'directory':
				os.system("mocp -P && mocp -c")
			
				for subdir, dirs, files in os.walk(fullpath):
					for file in sorted(files):
						musicfile = os.path.join(subdir, file)
						#print ("FILE: " + musicfile)
						os.system("mocp -a '" + musicfile + "'")

				os.system("mocp -p")
		else:
			# Just unpause:
			os.system("mocp -U")


	def pause(self):
		print ("Pausing")
		self.state = 'pause'
		#Album.objects.filter(playing=True).playing = False
		os.system('mocp -P')

	def prev(self):
		os.system('mocp -r')

	def next(self):
		os.system('mocp -f')

	def currentTrack(self):
		# Transforms mocp-info to JSON-hash.
		from django.http import JsonResponse

		#playingAlbum = Album.objects.filter(playing=True)

		proc = subprocess.Popen(["mocp", "-i"], stdout=subprocess.PIPE)
		(out, err) = proc.communicate()
		infoConsole = out.decode(encoding='utf-8').splitlines()

		infoReturn = {}

		#if playingAlbum: infoReturn['image'] = playingAlbum.image

		for line in infoConsole:
			key,value = line.split(': ')
			infoReturn[key] = value

		return JsonResponse(infoReturn)
