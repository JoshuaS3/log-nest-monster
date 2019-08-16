#!/usr/bin/env python3

# lognestmonster Copyright (c) 2019 Joshua 'joshuas3' Stockin
# <https://github.com/JoshuaS3/lognestmonster/>.


# This file is part of lognestmonster.

# lognestmonster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# lognestmonster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with lognestmonster. If not, see <https://www.gnu.org/licenses/>.

from utils import *
from format import *
from text import *

class Parser:
	screen = None
	clines = None
	ccols = None
	lines = None
	def __init__(self):
		self.screen = curses_window()
		self.get_size()

	def get_size(self):
		size = term_size()
		self.clines = size[0]
		self.ccols = size[1]

	def redraw(self):
		self.get_size()
		self.lines = self.lines[:self.clines] # limit output line count to screen line count
		curses_clear(self.screen)
		for line_index in range(0, len(self.lines)):
			self.lines[line_index] = str(self.lines[line_index])[:self.ccols]
		output = "\n".join(self.lines)
		self.screen.addstr(output)
		curses_refresh(self.screen)

	def get_input(self):
		input = getch()
		if input == UP: input = "up"
		elif input == DOWN: input = "down"
		elif input == LEFT: input = "left"
		elif input == RIGHT: input = "right"
		else: input = str(input).lower()
		return input

	def loop(self):
		input = None
		while True:
			self.get_size()
			
			screen_width = self.ccols - 1
			self.lines = [
				"lognestmonster - log_folder/",
				"Size: 9,608,560 bytes | Timestamp: 1565561768719",
				"192,000 Statements | 4,820 Events | 18 Unsaved Data Trees",
				pad(" STATEMENT 17 ", ":", screen_width),
				"v 4 ITEMS",
				"  1565561768752 - INFO - INIT - HELLO",
				"  1565561768752 - INFO - INIT - HELLO",
				"  v 4 ITEMS",
				"    1565561768752 - INFO - INIT - HELLO",
				"    1565561768752 - INFO - INIT - HELLO",
				"",
				"    1565561768752 - INFO - INIT - HELLO",
				"",
				"    1565561768752 - INFO - INIT - HELLO",
				"  1565561768752 - INFO - INIT - HELLO",
				"",
				"",
				"",
				"",
				"",
				pad(CONTROLS_MESSAGE, ":", screen_width)
			]
			self.redraw()

			input = self.get_input()

			if input == CTRLC or input == "q": # exit program on Ctrl + C or `q`
				break;


def argument_parse(argv):
	pass

def main():
	try:
		args = sys.argv
		if ("-v" in args):
			output(VERSION_MESSAGE)
		else:
			Parser().loop()
	finally:
		curses_reset()

if __name__ == "__main__":
	main()
