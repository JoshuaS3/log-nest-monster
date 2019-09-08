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
import time
from utils import *
from format import *
from text import *
from args import *
from parseargs import *
from read import *
from tui import *

def output_exit(error=None):
	exitcode = 0
	output(VERSION_SHORT)
	if error is not None: # print argument error is exists
		output(TEXT_RED + "error: " + RESET + error)
		exitcode = 1
	output(HELP_MESSAGE)
	exit(exitcode)

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
	ccols = screen_size[1]

	if display_help:
		output(VERSION_SHORT)

		output("usage: lognestmonster " + USAGE_MESSAGE)

		output()

		for paragraph in COMMAND_INFO.split("\n\n"):
			output_lines(wrap(paragraph, ccols))

		output()

		args = []

		div1 = int(ccols/3)
		div2 = int(ccols/3*2)
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
		if type(options) is str: # print argument error is exists
			output_exit(options)
		else:
			output_exit()

	positional = sys.argv[-1]
	if positional is not "-" and os.path.isfile(positional) is not True and os.path.isdir(positional) is not True:
		output_exit("file unknown '" + positional + "'")

	if positional is "-": positional = "stdin"

	if positional is "stdin":
		fd = sys.stdin
	else:
		try:
			fd = open(positional, "rb", buffering=8192)
		except:
			output_exit("unable to open file '" + positional + "'")

	if not is_status:
		p = TUI()
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
			r.filters = True
		else:
			r.filter_verbosity = [0, 1, 2, 3, 4, 5]

		if filter_after:
			try:
				r.filter_time_start = int(options["after"][0])
				r.filters = True
			except:
				output_exit("expected int for flag --after, got '" + options["after"][0] + "'")
		if filter_before:
			try:
				r.filter_time_end = int(options["before"][0])
				r.filters = True
			except:
				output_exit("expected int for flag --before, got '" + options["before"][0] + "'")

		if filter_tag:
			r.filter_tag = str(options["tag"][0])
			r.filters = True
		if positional is not "stdin": r.size()
		else: r.seekable = False
		output("File scan in progress...")
		s = time.time()
		def update():
			if r.statement_count % 1000 == 0:
				output("{0} statements | {1} events | {2} bad bytes | {3}%".format(r.statement_count, r.event_count, r.bad_bytes, round((r.position/r.file_size)*1000)/10), end="\r")
		r.onupdate(update)
		r.scan()
		output("{0} statements | {1} events | {2} bad bytes | {3}%".format(r.statement_count, r.event_count, r.bad_bytes, round((r.position/r.file_size)*1000)/10))
		elapsed = time.time() - s
		if elapsed > 1:
			output("Finished in {0} seconds".format(elapsed))

	fd.close()


if __name__ == "__main__":
	main()
