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

import struct
import os

STATEMENT_START = 0
STATEMENT_END = 1
EVENT_START = 2
EVENT_END = 3

def ulonglong(bytestr):
	return struct.unpack("@Q", bytestr)[0]
def uchar(charv):
	return struct.unpack("@B", charv)[0]
def ushort(shortv):
	return struct.unpack("@H", shortv)[0]


class NestableProto:
	parent = None

class NestProto:
	pushed = []

class StatementProto(NestableProto):
	verbosity = 0
	timestamp = 0
	pos = 0
	def __init__(self):
		self.verbosity = 0
		self.timestamp = 0
		self.pos = 0
		self.parent = None
		self.pushed = []

class EventProto(NestProto, NestableProto):
	def __init__(self):
		self.parent = None
		self.pushed = []


class Reader:
	fd = None

	version = 0
	timestamp = 0

	objects = {}

	event_count = 0
	statement_count = 0

	file_size = 0
	position = 0

	def __init__(self, fd):
		self.fd = fd

		self.version = 0
		self.timestamp = 0

		self.objects = {} # key = position in file, value = True for statement, False for event

		self.event_count = 0
		self.statement_count = 0

		self.file_size = 0
		self.position = 0

		self.size()
		self.scan()

	def size():
		self.fd.seek(0, os.SEEK_END) # go to end of file and get position
		newsize = self.fd.tell()
		self.fd.seek(self.position) # return to previous position

		diff = self.file_size - newsize
		self.file_size = newsize
		return diff > 0

	def scan(): # scan for events and statements from self.position to the end of file
		if self.position == 0: # if it's the start of the file, grab version and timestamp
			version_byte = self.fd.read(1)
			self.version = uchar(version_byte)
			timestamp_bytes = self.fd.read(8)
			self.timestamp = ulonglong(timestamp_bytes)
			self.position = self.fd.tell()

		current_statement = None
		current_event = None
		if self.position < self.file_size:
			self.objects[self.position:self.file_size] = None
			while self.position < self.file_size:
				pass

