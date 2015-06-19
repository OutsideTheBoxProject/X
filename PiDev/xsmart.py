# global imports
import pygame
from pygame.locals import *
import PIL
from PIL import Image
import RPi.GPIO as GPIO

import sys, os, random

# local imports
import constants as con

# global variables
screen = None
mode = con.STORYMODE
picPool = []
vidPool = []
storyShown = False
waiting = 0
announce = True
movie = None
playing = False
movieScreen = None
clock = None

# implementation

# get an array of available pictures up to the maxpic number
def get_pictures():
	return random.sample(os.listdir(con.PICS), con.MAXPICS)
	
# returns an array of available videos up to the maxvid number
def get_videos():
	return random.sample(os.listdir(con.VIDEOS), con.MAXVIDS)

# this declutters the main function
def setup():
	# setup proper logging into a txt file, if wanted
	if con.STDOUT == con.STDOUTVIAFILE:
		sys.stdout = open(con.STDOUTFILE, 'a')
		sys.stderr = open(con.STDOUTFILE, 'a')
		
	# setup the screen
	global screen
	pygame.init()
	screen = pygame.display.set_mode((con.SCREENWIDTH, con.SCREENHEIGHT), pygame.FULLSCREEN)
	flush_screen()
	
	# setup buttons
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(con.ADVANCEBUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(con.MODEBUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	
	# setup picture pool
	global picPool, vidPool
	picPool = get_pictures()
	vidPool = get_videos()
	
# mode announcing made easy
def announce_mode(modeText):
	global screen, announce
	screen.fill(con.BACKGROUNDCOLOUR)
	font = pygame.font.Font(con.FONT, 60)
	text = font.render(modeText, 1, con.ORANGE)
	screen.blit(text, (con.SCREENWIDTH/3.5, con.SCREENHEIGHT/3))
	pygame.display.flip()
	announce = False

# announces the storymode to the screen
def announce_storymode():	
	announce_mode("Geschichten!")

# announces the videomode to the screen
def announce_videomode():
	announce_mode("Neue Filme!")

# does all the setup for finishing a movie
def finish_movie():
	global movie
	movie.stop()
	screen = pygame.display.set_mode((con.SCREENWIDTH, con.SCREENHEIGHT), pygame.FULLSCREEN)



# testing for keyboard or button input
def test_for_input():
	global mode, picPool, storyShown, announce, movie
	toggle = True
	while (GPIO.input(con.MODEBUTTON)):
		if toggle: 
			if mode == con.VIDEOMODE:
				mode = con.STORYMODE
				announce = True
				if not movie == None:
					movie.stop()
				picPool = get_pictures()
				storytime()
			elif mode == con.STORYMODE:
				mode = con.VIDEOMODE
				announce = True
				videotime()
			toggle = False
			
	while (GPIO.input(con.ADVANCEBUTTON)):
		if toggle:
			if mode == con.VIDEOMODE:
				if not movie == None:
					movie.stop()
				videotime()
			elif mode == con.STORYMODE:
				storytime()
			toggle = False
					
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				print "Goodbye."
				exit()
	
# suggest a pause
def suggest_pause(pause):
	global screen
	screen.fill(con.BACKGROUNDCOLOUR)
	font = pygame.font.Font(con.FONT, 40)
	text = font.render("Ich habe gerade keine " + pause + " mehr.", 1, con.BLUE)
	screen.blit(text, (con.SCREENWIDTH/8, con.SCREENHEIGHT/4))
	text = font.render("Mach vielleicht mal eine Pause.", 1, con.BLUE)
	screen.blit(text, (con.SCREENWIDTH/6, con.SCREENHEIGHT/3))
	pygame.display.flip()

# creates a plain background again after messages
def flush_screen():
	global screen
	screen.fill(con.BACKGROUNDCOLOUR)
	pygame.display.flip()
	
# shows a random picture in the current picPool
def storytime():
	global picPool, screen, waiting, announce
	if announce:
		announce_storymode()
	elif len(picPool) > 0 and waiting == 0:
		if len(picPool) == con.MAXPICS:
			flush_screen()	
		pic = random.choice(picPool)	
		screen.blit(pygame.image.load(con.PICS + pic), (0,0))
		pygame.display.flip()	
		picPool.remove(pic)
	else: 
		if waiting < con.WAITCTR:
			suggest_pause("Bilder")
			waiting = waiting + 1
		else: 
			waiting = 0
			picPool = get_pictures()	
			
# shows a random video in the current vidPool
def videotime():
	global vidPool, screen, waiting, announce, movie, movieScreen, clock
	if announce: 
		announce_videomode()
	elif len(vidPool) > 0 and waiting == 0:
		vid = random.choice(vidPool)
		clock = pygame.time.Clock()
		movie = pygame.movie.Movie(con.VIDEOS + vid)
		screen = pygame.display.set_mode(movie.get_size(), pygame.FULLSCREEN)
		movieScreen = pygame.Surface(movie.get_size()).convert()
		movie.set_display(movieScreen)
		movie.play()
		vidPool.remove(vid)
	else:
		if waiting < con.WAITCTR:
			suggest_pause("Filme")
			waiting = waiting + 1
		else:
			waiting = 0
			vidPool = get_videos()
		
			
# main function
def main():
	global storyShown, movieScreen, screen, clock
	setup()	
	# for now only a way to exit
	while True:
		if mode == con.STORYMODE and not storyShown:
			storytime()
			storyShown = True
		if playing:
			screen.blit(movieScreen, (0,0))
			pygame.display.flip()
			clock.tick(con.FPS)
		test_for_input()

main()

