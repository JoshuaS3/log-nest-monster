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
		"description": DESCRIPTION_HELP
	},
	"version": {
		"indicators": ["--version"],
		"description": DESCRIPTION_VERSION
	},

	# Data

	"status": {
		"indicators": ["-s", "--status"],
		"description": DESCRIPTION_STATUS
	},

	# Verbosity levels

	"errors": {
		"indicators": ["-e", "--errors"],
		"description": DESCRIPTION_ERRORS
	},
	"warnings": {
		"indicators": ["-w", "--warnings"],
		"description": DESCRIPTION_WARNINGS
	},
	"info": {
		"indicators": ["-i", "--info"],
		"description": DESCRIPTION_INFO
	},
	"debug": {
		"indicators": ["-d", "--debug"],
		"description": DESCRIPTION_DEBUG
	},
	"verbose": {
		"indicators": ["-v", "--verbose"],
		"description": DESCRIPTION_VERBOSE
	},
	"veryverbose": {
		"indicators": ["-vv", "--veryverbose"],
		"description": DESCRIPTION_VERYVERBOSE
	},

	# filters

	"after": {
		"indicators": ["-a", "--after"],
		"description": DESCRIPTION_AFTER
	},
	"before": {
		"indicators": ["-b", "--before"],
		"description": DESCRIPTION_BEFORE
	},
	"tag": {
		"indicators": ["-t", "--tag"],
		"description": DESCRIPTION_TAG
	},
	"statement": {
		"indicators": ["-c"],
		"description": DESCRIPTION_STATEMENT
	},
	"event": {
		"indicators": ["-q"],
		"description": DESCRIPTION_EVENT
	},

	# other

	"follow": {
		"indicators": ["-f", "--follow"],
		"description": DESCRIPTION_FOLLOW
	},
	"stdin": {
		"indicators": ["-x", "--stdin"],
		"description": DESCRIPTION_STDIN
	}
}
