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

VERSION_SHORT = """lognestmonster/0.1.0"""

VERSION_MESSAGE = """lognestmonster/0.1.0 Copyright (c) 2019 Joshua 'joshuas3' Stockin
Licensed under version 3 of the GNU General Public License
<https://github.com/JoshuaS3/lognestmonster/>
"""

# Help screen information

HELP_MESSAGE = "Run with --help to display usage information"
USAGE_MESSAGE = "Usage: lognestmonster [OPTIONS] <log_directory>"

DESCRIPTION_HELP = "Displays program description and a list of valid options and other arguments"
DESCRIPTION_VERSION = "Displays program information about copyright and the version"

DESCRIPTION_STATUS = "Reads the directory and outputs file and log metadata for each log tree"

DESCRIPTION_ERRORS = "Omits all statements besides errors. Stackable with other verbosity level commands"
DESCRIPTION_WARNINGS = "Omits all statements besides warnings. Stackable with other verbosity level commands"
DESCRIPTION_INFO = "Omits all statements besides those with verbosity type 'info'. Stackable with other verbosity level commands"
DESCRIPTION_DEBUG = "Omits all statements besides those with verbosity type 'debug'. Stackable with other verbosity level commands"
DESCRIPTION_VERBOSE = "Omits all statements besides those with verbosty type 'verbose'. Stackable with other verbosity level commands"
DESCRIPTION_VERYVERBOSE = "Omits all statements besides those with verbosity type 'veryverbose'. Stackable with other verbosity level commands"

DESCRIPTION_BEFORE = "Limits log results to before a certain timestamp"
DESCRIPTION_AFTER = "Limits log results to after a certain timestamp"
DESCRIPTION_TAG = "Limits log results to a tag"
DESCRIPTION_STATEMENT = "Limits log results to a numbered statement"
DESCRIPTION_EVENT = "Limits log results to a numbered event and its children"

DESCRIPTION_TAIL = "Provides a live scrolling view of the log tree stream, similar to the 'tail' command"

# TUI messages

HEADER_MESSAGE = "lognestmonster - {0}"

METADATA_MESSAGE = "Size: {0} bytes | Timestamp: {1}"

DATA_MESSAGE_DEFAULT = "{0} Statements | {0} Events | {0} Unsaved Data Trees"

CONTROLS_MESSAGE = " press q to exit | arrow keys to move, expand, collapse "
