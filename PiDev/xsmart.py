# Hardware Setup:
# GIPO  (BCM style notation)
# 0     SDA Real Time Clock
# 1     SCL Real Time Clock
# 4     Pi Supply (pin 7)
# 14    Pi Supply (pin 8)
# 17    Mode Button
# 22    Advance Button
# 3.3V  both Buttons 17 / 22 (active high, internal pull down resistor)
# 5V    VCC Real Time Clock
# GND   GND Real Time Clock

# global imports
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
from pyomxplayer import OMXPlayer

import sys, os, random, time

# local imports
import constants as con
import logging as log

# global variables
screen = None
mode = con.STORYMODE
picPool = []
vidPool = []
storyShown = False
waiting = 0
announce = True
omx = None
playing = False

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
	haveScreen = False
	while not haveScreen:
		try:
			pygame.init()
			screen = pygame.display.set_mode((con.SCREENWIDTH, con.SCREENHEIGHT), pygame.FULLSCREEN)
			haveScreen = True
		except pygame.error, message:
			print "Cannot get screen, trying again in one second"
			time.sleep(1)
	flush_screen()
	pygame.mouse.set_visible(False)
	
	# setup buttons
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(con.ADVANCEBUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(con.MODEBUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	
	# setup picture pool
	global picPool, vidPool
	picPool = get_pictures()
	vidPool = get_videos()
	
	log.log_start_station()
	
# mode announcing made easy
def announce_mode(modeText):
	global screen, announce
	screen.fill(con.BACKGROUNDCOLOUR)
	font = pygame.font.Font(con.FONT, 60)
	text = font.render(modeText, 1, con.ORANGE)
	screen.blit(text, (con.SCREENWIDTH/4, con.SCREENHEIGHT/3))
	pygame.display.flip()
	announce = False

# announces the storymode to the screen
def announce_storymode():	
	announce_mode("Geschichten!")

# announces the videomode to the screen
def announce_videomode():
	announce_mode("Neue Filme!")
	
# toggles modes: 
def toggle_mode():
	global mode, picPool, announce, vidPool, omx
	if mode == con.VIDEOMODE:
		mode = con.STORYMODE
		if not omx == None:
			omx.stop()
		announce = True
		picPool = get_pictures()
		storytime()
	elif mode == con.STORYMODE:
		mode = con.VIDEOMODE
		announce = True
		vidPool = get_videos()
		videotime()
		
# advances picture or video
def advance():
	log.log_advance_button()
	if mode == con.VIDEOMODE:
		if not omx == None: 
			omx.stop()
		videotime()
	elif mode == con.STORYMODE:
		storytime()

# testing for keyboard or button input
def test_for_input():
	global mode, picPool, storyShown, announce, omx, vidPool, playing
	toggle = True
	if not playing:
		while (GPIO.input(con.MODEBUTTON)):
			if toggle: 
				toggle_mode()
				toggle = False
				log.log_switch_state(mode)
			
		while (GPIO.input(con.ADVANCEBUTTON)):
			if toggle:
				advance()
				toggle = False
					
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				print "Goodbye."
				exit()
				
			elif event.key == pygame.K_a: 
				advance()
			elif event.key == pygame.K_t:
				toggle_mode()
	
# suggest a pause
def suggest_pause(pause):
	global screen
	screen.fill(con.BACKGROUNDCOLOUR)
	font = pygame.font.Font(con.FONT, 40)
	text = font.render("Ich habe gerade keine " + pause + " mehr.", 1, con.BLUE)
	screen.blit(text, (con.SCREENWIDTH/10, con.SCREENHEIGHT/4))
	text = font.render("Mach vielleicht mal eine Pause.", 1, con.BLUE)
	screen.blit(text, (con.SCREENWIDTH/8, con.SCREENHEIGHT/3))
	pygame.display.flip()
	log.log_pause()

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
		log.log_next(pic)
	else: 
		if waiting < con.WAITCTR:
			suggest_pause("Bilder")
			waiting = waiting + 1
		else: 
			waiting = 0
			picPool = get_pictures()	
			announce = True 
			
# shows a random video in the current vidPool
def videotime():
	global vidPool, screen, waiting, announce, omx, playing
	if announce: 
		announce_videomode()
	elif len(vidPool) > 0 and waiting == 0:
		vid = random.choice(vidPool)
		omx = OMXPlayer(con.VIDEOS + vid, start_playback = True)
		vidPool.remove(vid)
		log.log_next(vid)
	else:
		if waiting < con.WAITCTR:
			suggest_pause("Filme")
			waiting = waiting + 1
		else:
			waiting = 0
			vidPool = get_videos()
			announce = True
			
# main function
def main():
	global storyShown, movieScreen, screen, clock, playing
	setup()	
	# for now only a way to exit
	while True:
		if mode == con.STORYMODE and not storyShown:
			storytime()
			storyShown = True
		test_for_input()

main()

