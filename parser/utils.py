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

# get character from stdin

try:
	import termios, sys, tty
	def getch(cbytes=1):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			buf = sys.stdin.read(cbytes).encode("utf-8")
			if buf == b"\x1b": # if escaped
				while True:
					ch = sys.stdin.read(1).encode("utf-8")
					buf += ch
					if ch.isalpha():
						break
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return buf
except ImportError: # Windows NT, no term control
	import msvrct
	def getch(cbyte=1):
		buf = b""
		for x in range(0, cbyte):
			buf += msvrct.getch().encode("utf-8")
		if buf == b"\x1b":
			while True:
				ch = msvrct.getch().encode("utf-8")
				buf += ch
				if ch.isalpha():
					break
		return buf

# array to string

def array_stringify(array):
	index = 0
	for i in array:
		array[index] = str(i)
		index += 1
	return array

# echo output

import sys
def output(*array, end="\n"):
	array = array_stringify(list(array))
	s = "".join(array)
	sys.stdout.write(s.rstrip() + end)

def output_lines(array):
	for line in array:
		output(line)

# terminfo stuff

from shutil import get_terminal_size
def term_size():
	os_ts = get_terminal_size((80, 24))
	lines = os_ts.lines
	cols = os_ts.columns
	if cols > 80: cols = 80
	return (lines, cols-1)

# drawing

import curses
def curses_window():
	# init curses
	screen = curses.initscr()
	curses.start_color()
	curses.use_default_colors()

	curses.init_pair(1, curses.COLOR_BLACK, -1)
	curses.init_pair(2, curses.COLOR_BLUE, -1)
	curses.init_pair(3, curses.COLOR_CYAN, -1)
	curses.init_pair(4, curses.COLOR_GREEN, -1)
	curses.init_pair(5, curses.COLOR_MAGENTA, -1)
	curses.init_pair(6, curses.COLOR_RED, -1)
	curses.init_pair(7, curses.COLOR_WHITE, -1)
	curses.init_pair(8, curses.COLOR_YELLOW, -1)

	# get screen size and create new window
	screen_size = term_size()

	# set cursor visibility to 0
	curses.curs_set(0)

	# set new window to current
	curses_refresh(screen)

	return screen

def curses_clear(screen):
	screen.clear()
	screen.touchwin()
	curses_refresh(screen)

def curses_refresh(screen):
	if screen.is_wintouched():
		screen.refresh()

def curses_reset():
	try:
		if not curses.isendwin():
			curses.endwin()
	except:
		pass
