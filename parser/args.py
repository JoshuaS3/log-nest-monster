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

from text import *

ARGUMENT_OPTIONS = {

	# Command meta

	"help": {
		"indicators": ["-h", "-?", "--help"],
		"description": DESCRIPTION_HELP,
		"valcount": 0
	},
	"version": {
		"indicators": ["--version"],
		"description": DESCRIPTION_VERSION,
		"valcount": 0
	},

	# Data

	"status": {
		"indicators": ["-s", "--status"],
		"description": DESCRIPTION_STATUS,
		"valcount": 0
	},

	# Verbosity levels

	"errors": {
		"indicators": ["-e", "--errors"],
		"description": DESCRIPTION_ERRORS,
		"valcount": 0
	},
	"warnings": {
		"indicators": ["-w", "--warnings"],
		"description": DESCRIPTION_WARNINGS,
		"valcount": 0
	},
	"info": {
		"indicators": ["-i", "--info"],
		"description": DESCRIPTION_INFO,
		"valcount": 0
	},
	"debug": {
		"indicators": ["-d", "--debug"],
		"description": DESCRIPTION_DEBUG,
		"valcount": 0
	},
	"verbose": {
		"indicators": ["-v", "--verbose"],
		"description": DESCRIPTION_VERBOSE,
		"valcount": 0
	},
	"veryverbose": {
		"indicators": ["-vv", "--veryverbose"],
		"description": DESCRIPTION_VERYVERBOSE,
		"valcount": 0
	},

	# filters

	"after": {
		"indicators": ["--after"],
		"description": DESCRIPTION_AFTER,
		"valcount": 1
	},
	"before": {
		"indicators": ["--before"],
		"description": DESCRIPTION_BEFORE,
		"valcount": 1
	},
	"tag": {
		"indicators": ["-t", "--tag"],
		"description": DESCRIPTION_TAG,
		"valcount": 1
	},
	"item": {
		"indicators": ["--item"],
		"description": DESCRIPTION_ITEM,
		"valcount": 1
	},

	# other

	"follow": {
		"indicators": ["-f", "--follow"],
		"description": DESCRIPTION_FOLLOW,
		"valcount": 0
	}
}
