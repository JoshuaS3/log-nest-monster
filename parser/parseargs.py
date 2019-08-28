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

from format import *
from args import *
# yeah, I know argparse is a thing, but I don't like it...

def get_arg_from_indicator(indicator):
	for option in ARGUMENT_OPTIONS:
		if indicator in ARGUMENT_OPTIONS[option]["indicators"]:
			return option
	return None

def get_arg_valcount(name):
	return ARGUMENT_OPTIONS[name]["valcount"]

def parseargs(argv):
	options = {}
	argn = 0
	while argn < len(argv):
		arg = argv[argn]
		if arg == "-":
			if argn == len(argv)-1: # if it's the last argument, allow it
				break
		opt = get_arg_from_indicator(arg)
		if argn is not len(argv) - 1 and opt is None: # is a flag/option but is not the Queue
			options = TEXT_RED + "error:" + RESET + " unknown flag/option '" + arg + "'"
			return options
		if opt in options:
			options = TEXT_RED + "error:" + RESET + " double definition of argument '" + arg + "'"
			return options
		if opt is not None: # opt _can_ be None due to the last argument being Queue
			valcount = get_arg_valcount(opt)
			if valcount > 0:
				options[opt] = []
				for i in range(1, valcount+1):
					if argn+1 < len(argv) - 1 and argv[argn+1].startswith("-") is not True:
						options[opt].append(argv[argn + 1])
						argn += 1
					else:
						options = TEXT_RED + "error:" + RESET + " argument '" + arg + "' requires " + \
								  str(valcount) + " " + (valcount is 1 and "value" or "values") + \
								  ", only " + str(i-1) + " " + (i-1 is 1 and "was" or "were") + " given"
						return options
			else:
				options[opt] = None
		argn += 1
	return options
