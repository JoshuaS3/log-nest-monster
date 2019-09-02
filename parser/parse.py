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

import os
import sys
from utils import *
from format import *
from text import *
from args import *
from parseargs import *
from read import *

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
			line_len = 0
			for string in line:
				# ("content string", "attributes string")
				content = string[0]

				self.screen.attrset(0)

				try:
					attr = string[1]
				except:
					attr = ""

				if "RESET" in attr: # set curses attributes based on attributes string
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

				print(line_len)
				self.screen.addstr(content[:self.ccols - line_len])
				self.screen.attrset(0)
				line_len += len(content)
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
				screen_width = self.ccols

				self.lines = [
					[(self.title + " - ", "RESET"), (self.folder_name, "BOLD YELLOW")],
					"Size: 235 bytes | Timestamp: 1565561768719",
					"7 Statements | 2 Events | 0 Unsaved Data Trees",
					pad(" STATEMENT 5 ", ":", screen_width),
					"",
					"[[LOG START]]",
					"v 7 ITEMS",
					tab("1565561768752 - INFO - INIT - HELLO"),
					tab("1565561768752 - INFO - INIT - HELLO"),
					tab("v 4 ITEMS"),
					tab("1565561768752 - INFO - INIT - HELLO", 2),
					tab("1565561768752 - INFO - INIT - HELLO", 2),
					"",
					[(tab("1565561768752 - INFO - INIT - HELLO", 2), "BOLD")],
					"",
					tab("1565561768752 - INFO - INIT - HELLO", 2),
					tab("1565561768752 - INFO - INIT - HELLO"),
					"",
					str(input),
					"[[LOG END]",
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
	options = parseargs(sys.argv[1:])

	display_help = "help" in options
	display_version = "version" in options
	is_status = "status" in options

	filter_errors = "errors" in options
	filter_warnings = "warnings" in options
	filter_info = "info" in options
	filter_debug = "debug" in options
	filter_verbose = "verbose" in options
	filter_veryverbose = "veryverbose" in options

	filter_after = "after" in options
	filter_before = "before" in options
	filter_tag = "tag" in options

	screen_size = term_size()
	clines = screen_size[0]
	ccols = screen_size[1] - 2

	if display_help:
		output(VERSION_SHORT)

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
		output(DESCRIPTION_PYTHON_VERSION)
		return
	elif display_version:
		output(VERSION_MESSAGE)
		return
	elif len(sys.argv) == 1 or type(options) is str: # argument error or no args passed
		exitcode = 0
		output(VERSION_SHORT)
		if type(options) is str: # print argument error is exists
			output(options)
			exitcode = 1
		output(HELP_MESSAGE)
		exit(exitcode)

	positional = sys.argv[-1]
	if positional is not "-" and os.path.isfile(positional) is not True and os.path.isdir(positional) is not True:
		output(VERSION_SHORT)
		output(TEXT_RED + "error:" + RESET + " file unknown '" + positional + "'")
		output(HELP_MESSAGE)
		exit(1)

	if positional is "-": positional = "stdin"

	if positional is "stdin":
		fd = sys.stdin
	else:
		try:
			fd = open(positional, "rb", buffering=8192)
		except:
			output(TEXT_RED + "error:" + RESET + " unable to open file")
			exit(1)

	if not is_status:
		p = Parser()
		p.folder_name = positional
		p.loop()
	else:
		r = Reader(fd)

		filter_verbosity_levels = []
		if filter_errors:
			filter_verbosity_levels.append(5)
		if filter_warnings:
			filter_verbosity_levels.append(4)
		if filter_info:
			filter_verbosity_levels.append(0)
		if filter_debug:
			filter_verbosity_levels.append(1)
		if filter_verbose:
			filter_verbosity_levels.append(2)
		if filter_veryverbose:
			filter_verbosity_levels.append(3)
		if filter_verbosity_levels != []:
			r.filter_verbosity = filter_verbosity_levels
		else:
			r.filter_verbosity = [0, 1, 4, 5]

		if filter_after:
			try:
				r.filter_time_start = int(options["after"][0])
			except:
				output(VERSION_SHORT)
				output(TEXT_RED + "error:" + RESET + " expected int for flag --after, got '" + options["after"][0] + "'")
				output(HELP_MESSAGE)
				exit(1)
		if filter_before:
			try:
				r.filter_time_end = int(options["before"][0])
			except:
				output(VERSION_SHORT)
				output(TEXT_RED + "error:" + RESET + " expected int for flag --before, got '" + options["before"][0] + "'")
				output(HELP_MESSAGE)
				exit(1)

		if filter_tag:
			r.filter_tag = str(options["tag"][0])
		if positional is not "stdin": r.size()
		def update():
			print("bad bytes: {0}".format(r.bad_bytes), end="\r")
		r.onupdate(update)
		r.scan()
		print("bad bytes: {0}".format(r.bad_bytes))

	fd.close()


if __name__ == "__main__":
	main()
