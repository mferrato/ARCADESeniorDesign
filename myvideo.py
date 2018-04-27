import os, signal, sys, subprocess

def term_received(n, stack):
	os.unlink(pidfile)
	sys.exit(0)
	return

signal.signal(signal.SIGTERM, term_received) 

#os.system('omxplayer /home/pi/Desktop/video_1.mp4 --loop')
video = subprocess.Popen(['omxplayer','video_1.mp4'])
scriptpid = str(os.getpid())
videopid = str(video.pid)
print(scriptpid)
print(videopid)
pidfile ="/var/run/myvideo.pid"

if os.path.isfile(pidfile):
	print "%s already exists, exiting" % pidfile
#else:
#	file(pidfile, 'w').write(pid)


