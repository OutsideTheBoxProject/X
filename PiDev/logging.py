import constants as con
import os, time

# this is just a collection of logging functions in order to have them
# not clogging the main file
# most of them are only used during evaluation anyway 

# append a single line at the end of a text file
def append_line(filename, line):
	with open(filename, "a") as f:
		f.write(line + "\n")

# get the contents of a file as an array of lines
def get_lines(filename):
	with open(filename) as f:
		return f.readlines()
			
# get the correctly formatted timestamp for the local time	
def get_cur_timestamp():
	return time.strftime("%Y-%m-%d %H:%M:%S")

# returns the correctly formatted timestamp for the day
def get_date_timestamp():
	return time.strftime("%Y-%m-%d")
	
# formats the info with timestamp and delimiter
def get_line(info, detail=""):
	line = []
	line.append(get_cur_timestamp())
	line.append(info)
	line.append(detail)
	return ",".join(line)

# logging xsmart starting
def log_start_station():
	append_line(con.XSMARTLOG, get_line("starting xsmart"))

# logging a state switch
def log_switch_state(state):
	if state == con.VIDEOMODE:
		append_line(con.XSMARTLOG, get_line("switching from storymode to videomode"))
	elif state == con.STORYMODE:
		append_line(con.XSMARTLOG, get_line("switching from videomode to storymode"))
		
# logging a pause suggestion
def log_pause():
	append_line(con.XSMARTLOG, get_line("suggesting a pause"))
	
# logging successful display of things
def log_next(what):
	append_line(con.XSMARTLOG, get_line("displaying " + what))
	
# logging interaction with the advance button
def log_advance_button():
	append_line(con.XSMARTLOG, get_line("advance button has been pressed"))
