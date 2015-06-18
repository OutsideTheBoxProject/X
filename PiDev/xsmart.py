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
storyShown = False

# implementation


# get an array of all available pictures
def get_all_pictures():
	return os.listdir(con.PICS)
	

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
	screen.fill(con.BACKGROUNDCOLOUR)
	pygame.display.flip()
	
	# setup buttons
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(con.ADVANCEBUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(con.MODEBUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	
	# setup picture pool
	global picPool
	picPool = get_all_pictures()
	
	

# testing for keyboard or button input
def test_for_input():
	global mode
	toggle = True
	while (GPIO.input(con.MODEBUTTON)):
		if toggle: 
			if mode == con.VIDEOMODE:
				print "here we would switch the mode to the picture mode."
				mode = con.STORYMODE
			elif mode == con.STORYMODE:
				print "here we would switch the mode to the video mode."
				mode = con.VIDEOMODE
			toggle = False
			
	while (GPIO.input(con.ADVANCEBUTTON)):
		if toggle:
			if mode == con.VIDEOMODE:
				print "here we would advance to the next video"
			elif mode == con.STORYMODE:
				storytime()
			toggle = False
					
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				print "Goodbye."
				exit()
	
# suggest picture pause
def no_pictures():
	global screen
	screen.fill(con.BACKGROUNDCOLOUR)
	
	
# shows a random picture in the current picPool
def storytime():
	global picPool, screen
	if len(picPool) > 0:
		pic =  random.choice(picPool)	
		screen.blit(pygame.image.load(con.PICS + pic), (0,0))
		pygame.display.flip()	
		picPool.remove(pic)
	else: 
		print "picPool empty"
		
			
# main function
def main():
	global storyShown
	setup()	
	# for now only a way to exit
	while True:
		if mode == con.STORYMODE and not storyShown:
			storytime()
			storyShown = True
		test_for_input()

main()

