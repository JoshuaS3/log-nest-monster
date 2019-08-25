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


# ANSI codes for output

RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINED = "\033[4m"
CONTRAST = "\033[7m"

TEXT_RED = "\033[91m"
TEXT_GREEN = "\033[92m"
TEXT_YELLOW = "\033[93m"
TEXT_MAGENTA = "\033[95m"
TEXT_CYAN = "\033[96m"

BACK_RED = "\033[101m"
BACK_GREEN = "\033[102m"
BACK_YELLOW = "\033[103m"
BACK_MAGENTA = "\033[105m"
BACK_CYAN = "\033[106m"

UP = "\x1b[A"
DOWN = "\x1b[B"
RIGHT = "\x1b[C"
LEFT = "\x1b[D"
CTRLC = "\x03"


# wrap lines

def wrap(string, width, delimiter=None):
	string_length = len(string)
	if string_length <= width: return [string.replace(delimiter or "\0", " ")]
	lines = []
	line = ""
	words = string.split(delimiter)
	for word in words:
		line += " "
		word_length = len(word)
		if word_length == 0: continue
		if word_length > width:
			for char in word:
				line += char
				line = line.strip()
				if len(line) == width:
					lines.append(line)
					line = ""
			continue
		if len(line) + word_length > width:
			lines.append(line)
			line = word
		else:
			line += word
			line = line.strip()
	line = line.strip()
	if len(line) > 0:
		lines.append(line)
	return lines

def columnize(items, width):
	string = ""
	for item in items:
		length = int(item[0])
		content = item[1].strip()[:length]
		string += content.ljust(length, " ")
	return string[:width]

def pad(string, padding, width):
	length = len(string)
	if length >= width: return string[:width]
	padding_length = int((width-length)/2)
	return (padding*padding_length + string + padding*padding_length)[:width]

def margin(string, m=" "):
	return m + string + m

def expand(string1, string2, width):
	if len(string1) >= width: return string1[:width]
	full = string1 + string2
	if len(full) >= width: return full[:width]
	left = width - len(full)
	return (string1 + " "*left + string2)[:width]
