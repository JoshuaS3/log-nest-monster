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

def get_arg_description(name):
	return ARGUMENT_OPTIONS[name]["description"]

def parseargs(argv):
	options = {}
	argn = 0
	while argn < len(argv):
		arg = argv[argn]
		if arg == "-":
			argn += 1
			continue
		opt = get_arg_from_indicator(arg)
		if arg.startswith("-") and opt is None: # is a flag/option but is not known
			options = TEXT_RED + "error:" + RESET + " unknown flag/option '" + arg + "'"
			break
		options[opt] = None
		argn += 1
	return options
