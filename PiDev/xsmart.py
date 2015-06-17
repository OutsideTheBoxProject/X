# global imports
import pygame
from pygame.locals import *
import PIL
from PIL import Image

import sys, os

# local imports
import constants as con

# global variables
screen = None

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

# testing whether the esc key has been pressed	
def test_for_exit():	
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
		test_for_exit()

main()

