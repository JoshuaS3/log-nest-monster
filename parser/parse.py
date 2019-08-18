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
from args import *

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
		curses_clear(self.screen)
		l = 0
		for line in self.lines:
			if l == self.clines: break
			self.screen.move(l, 0)
			s = ""
			for string in line:
				content = string[0]
				s += content

				self.screen.attrset(0)

				try:
					attr = string[1]
				except:
					attr = ""

				if "RESET" in attr:
					self.screen.attron(curses.color_pair(0))
				else:
					if "BLACK" in attr:
						self.screen.attron(curses.color_pair(1))
					if "BLUE" in attr:
						self.screen.attron(curses.color_pair(2))
					if "CYAN" in attr:
						self.screen.attron(curses.color_pair(3))
					if "GREEN" in attr:
						self.screen.attron(curses.color_pair(4))
					if "MAGENTA" in attr:
						self.screen.attron(curses.color_pair(5))
					if "RED" in attr:
						self.screen.attron(curses.color_pair(6))
					if "WHITE" in attr:
						self.screen.attron(curses.color_pair(7))
					if "YELLOW" in attr:
						self.screen.attron(curses.color_pair(8))
					if "BOLD" in attr:
						self.screen.attron(curses.A_BOLD)
					if "STANDOUT" in attr:
						self.screen.attron(curses.A_STANDOUT)
					if "UNDERLINE" in attr:
						self.screen.attron(curses.A_UNDERLINE)

				self.screen.addstr(content[:self.ccols - len(s)])
				self.screen.attrset(0)
			l += 1
		curses_refresh(self.screen)

	def get_input(self):
		input = getch()
		if input == UP: input = "up"
		elif input == DOWN: input = "down"
		elif input == LEFT: input = "left"
		elif input == RIGHT: input = "right"
		elif input == CTRLC: input = "exit"
		else: input = str(input).lower()
		return input

	folder_name = "log_1565561768719"
	divider = " | "
	title = TITLE

	def loop(self):
		def tab(string, count=1):
			return "  "*count + string
		input = None
		try:
			while True:
				self.get_size()
				screen_width = self.ccols - 2

				self.lines = [
					[(self.title + " - ", "RESET"), (self.folder_name, "BOLD YELLOW")],
					"Size: 235 bytes | Timestamp: 1565561768719",
					[("7 Statements | 2 Events | 0 Unsaved Data Trees", "")],
					pad(" STATEMENT 5 ", ":", screen_width),
					"v 7 ITEMS",
					tab("1565561768752 - INFO - INIT - HELLO"),
					tab("1565561768752 - INFO - INIT - HELLO"),
					tab("v 4 ITEMS"),
					tab("1565561768752 - INFO - INIT - HELLO", 2),
					tab("1565561768752 - INFO - INIT - HELLO", 2),
					"",
					[(tab("", 2), "RESET"), ("1565561768752 - INFO - INIT - HELLO", "BOLD")],
					"",
					tab("1565561768752 - INFO - INIT - HELLO", 2),
					tab("1565561768752 - INFO - INIT - HELLO"),
					"",
					str(input),
					"",
					"",
					"",
					"",
					"",
					"",
					pad(margin(CONTROLS_MESSAGE), ":", screen_width)
				]
				self.redraw()

				input = self.get_input()

				if input == "exit" or input == "q": # exit program on Ctrl + C or `q`
					break;
		finally:
			curses_reset()

def main():
	options = []#argument_parse(sys.argv)

	display_help = "help" in options
	display_version = True#"version" in options
	is_status = "status" in options

	screen_size = term_size()
	clines = screen_size[0]
	ccols = screen_size[1] - 2

	if display_help:
		output_lines(VERSION_SHORT)

		usage = []
		line = "usage: lognestmonster "
		x = len(line)
		width = ccols - x
		wrapped = wrap(USAGE_MESSAGE, width, "&")
		for l in wrapped:
			line += l
			usage.append(line)
			line = (" "*x)
		output_lines(usage)

		output()

		for paragraph in COMMAND_INFO.split("\n\n"):
			output_lines(wrap(paragraph, ccols))

		output()

		args = []

		div1 = ccols/3
		div2 = ccols/3*2
		for arg in ARGUMENT_OPTIONS:
			arg_lines = []
			indicators = wrap(", ".join(ARGUMENT_OPTIONS[arg]["indicators"]), div1)
			description = wrap(ARGUMENT_OPTIONS[arg]["description"], div2)
			l1 = indicators[0]
			z = 0
			for line in description:
				try:
					l1 = indicators[z]
				except:
					l1 = ""
				z += 1
				l = columnize([(div1, l1), (div2, line)], ccols)
				arg_lines.append(l)
			args += arg_lines

		output_lines(args)
		output()
		return
	elif display_version:
		output(VERSION_MESSAGE)
	else:
		output(VERSION_SHORT)
		output(HELP_MESSAGE)

if __name__ == "__main__":
	main()
