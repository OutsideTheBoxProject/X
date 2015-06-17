# global imports
import pygame
from pygame.locals import *
import PIL
from PIL import Image
import RPi.GPIO as GPIO

import sys, os

# local imports
import constants as con

# global variables
screen = None
mode = con.STORYMODE

# implementation

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
				print "here we would advance to the next picture"
			toggle = False
					
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				print "Goodbye."
				exit()
	
	
			
# main function
def main():
	setup()	
	# for now only a way to exit
	while True:
		if mode == con.STORYMODE:
			print "storytimes"
		test_for_input()

main()

