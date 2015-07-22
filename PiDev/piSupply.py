# Import the libraries to use time delays, send os commands and access GPIO pins
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM) # Set pin numbering to GPIO numbering
GPIO.setup(4, GPIO.IN) # Setup GPIO 4 as an input
while True: # Setup a while loop to wait for a button press
    if(GPIO.input(4)): # Setup an if loop to run a shutdown command when button press sensed
        os.system("sudo shutdown -h now") # Send shutdown command to os
        break
    time.sleep(0.3) # Allow a sleep time of 1 second to reduce CPU usage
