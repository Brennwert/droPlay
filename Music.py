import os
import subprocess


class Music:

	def __init__(self):
		from musiControl.models import Album
		os.system("mocp -P -o repeat")
		self.state = 'pause'

		try:
			loading = Album.objects.get(state="loading")
			loading.state = ""
			loading.save()
		except:
			pass


	def playingOrPaused(self):
            if os.system("mocp -i | grep 'State: P'") == 0:
                return 1
            return 0

	def play(self, obj = None):		
		from musiControl.models import Album

		if obj:
			obj.state = 'loading'
			obj.save()
			self.path = obj.path

			try:
				pausedTitle = Album.objects.get(state="paused")
				pausedTitle.state = ""
				pausedTitle.save()
			except Album.DoesNotExist:
				pausedTitle = None
			
			fullpath = self.root + obj.path
			print("Playing " + fullpath)

			if obj.type == 'playlist':
				os.system("mocp -c -a '" + fullpath + "' -p");

			elif obj.type == 'directory':
				os.system("mocp -P && mocp -c")
			
				for subdir, dirs, files in os.walk(fullpath):
					for file in sorted(files):
						musicfile = os.path.join(subdir, file)
						#print ("FILE: " + musicfile)
						os.system("mocp -a '" + musicfile + "'")

				os.system("mocp -p")

			obj.state = "playing"
			obj.save()
		else:
			# Just unpause:
			os.system("mocp -U")

			try:
				pausedTitle = Album.objects.get(state="paused")
				pausedTitle.state = "playing"
				pausedTitle.save()
			except Album.DoesNotExist:
				pausedTitle = None

		self.state = 'play'


	def pause(self):
		print ("Pausing")
		self.state = 'pause'

		os.system('mocp -P')

		from musiControl.models import Album
		playingTitle = Album.objects.get(state="playing")
		playingTitle.state = "paused"
		playingTitle.save()

	def prev(self):
		os.system('mocp -r')

	def next(self):
		os.system('mocp -f')

	def currentTrack(self):
		# Transforms mocp-info to JSON-hash.
		from django.http import JsonResponse
		from musiControl.models import Album

		#playingAlbum = Album.objects.filter(playing=True)

		proc = subprocess.Popen(["mocp", "-i"], stdout=subprocess.PIPE)
		(out, err) = proc.communicate()
		infoConsole = out.decode(encoding='utf-8').splitlines()

		infoReturn = {}

		#if playingAlbum: infoReturn['image'] = playingAlbum.image

		#infoReturn['status'] = self.state

		try:
			loading = Album.objects.get(state="loading")
			infoReturn['loading'] = 1
		except Album.DoesNotExist:
			infoReturn['loading'] = 0

		for line in infoConsole:
			key,value = line.split(': ')
			infoReturn[key] = value

		return JsonResponse(infoReturn)
