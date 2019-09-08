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
from text import *

class TUI:
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

				out = content[:self.ccols - line_len]
				self.screen.addstr(out)
				self.screen.attrset(0)
				line_len += len(out)
			l += 1
		curses_refresh(self.screen)

	def get_input(self):
		input = getch()
		if input == UP: input = "up"
		elif input == DOWN: input = "down"
		elif input == LEFT: input = "left"
		elif input == RIGHT: input = "right"
		elif input == CTRLC: input = "exit"
		else: input = input.decode("utf-8").lower()
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
					pad(margin("STATEMENT 5"), ":", screen_width),
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