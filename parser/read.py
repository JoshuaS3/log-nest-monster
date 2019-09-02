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
import resource
import time
import sys

STATEMENT_START = 0
STATEMENT_END = 1
EVENT_START = 2
EVENT_END = 3

VERBOSITY_LEVELS = {
	0: "INIT",
	1: "DEBUG",
	2: "VERBOSE",
	3: "VERYVERBOSE",
	4: "WARNING",
	5: "ERROR"
}

def ulonglong(bytestr):
	return struct.unpack("@Q", bytestr)[0]
def uchar(charv):
	return struct.unpack("@B", charv)[0]
def ushort(shortv):
	return struct.unpack("@H", shortv)[0]


class EventProto:
	parent = None
	pushed = []
	def __init__(self):
		self.parent = None
		self.pushed = []

class Reader:
	fd = None

	version = 0
	timestamp = 0

	top_level = []

	event_count = 0
	statement_count = 0

	file_size = 0
	position = 0
	bad_bytes = 0

	filter_time_start = -1
	filter_time_end = -1
	filter_verbosity = -1
	filter_tag = -1

	def __init__(self, fd):
		self.fd = fd

		self.version = 0
		self.timestamp = 0

		self.top_level = []

		self.event_count = 0
		self.statement_count = 0

		self.file_size = 0
		self.position = 0
		self.bad_bytes = 0

		self.filter_time_start = -1
		self.filter_time_end = -1
		self.filter_verbosity = -1
		self.filter_tag = -1

	def size(self):
		self.fd.seek(0, os.SEEK_END) # go to end of file and get position
		newsize = self.fd.tell()
		self.fd.seek(self.position) # return to previous position

		is_diff = self.file_size is not newsize
		self.file_size = newsize
		return is_diff

	def pos(self):
		self.position = self.fd.tell()
		return self.position

	def seek(self, position):
		self.position = position
		self.fd.seek(self.position)

	def read(self, byte_count):
		data = self.fd.read(byte_count)
		if len(data) == byte_count:
			return data
		else:
			return False

	def scan(self): # scan for events and statements from self.position to the end of file
		print()
		print("beginning file scan")
		print("file size: {0}".format(self.file_size))
		print()

		s = time.time()

		if self.position == 0: # if it's the start of the file, grab version and timestamp
			self.version = uchar(self.read(1))
			self.timestamp = ulonglong(self.read(8))

		current_statement = None
		current_event = None

		if self.position < self.file_size: # if the seeker is before EOF
			while self.position < self.file_size: # while the seeker is before EOF
				in_byte = uchar(self.read(1)) # read 1 byte

				if in_byte == STATEMENT_START: # the byte indicates a statement's start, begin interpreting
					self.statement_count += 1

					new_statement = self.position

					timestamp = ulonglong(self.read(8))
					verbosity = uchar(self.read(1))
				
					tag_size = uchar(self.read(1))
					tag = self.read(tag_size).decode("utf-8")
				
					append = True
					if self.filter_time_start is not -1:
						if timestamp < self.filter_time_start: append = False
					if self.filter_time_end is not -1:
						if timestamp > self.filter_time_end: append = False
					if self.filter_verbosity is not -1:
						if verbosity is not self.filter_verbosity: append = False
					if self.filter_tag is not -1:
						if tag is not self.filter_tag: append = False

					message_size = ushort(self.read(2))
					self.seek(self.pos() + message_size) # ignore the message
					
					while uchar(self.read(1)) is not STATEMENT_END and self.pos() < self.file_size:
						self.bad_bytes += 1

					if append:
						if current_event is not None:
							current_event.pushed.append(new_statement)
						else:
							self.top_level.append(new_statement)

				elif in_byte == EVENT_START: # the byte indicates an event's start, create an event
					self.event_count += 1
					new_event = EventProto()
					if current_event is not None: # if an event exists, push the new event to it
						new_event.parent = current_event
						current_event.pushed.append(new_event)
					current_event = new_event


				elif in_byte == EVENT_END: # the byte indicates an event's end, close event if exists
					if current_event is not None: # if an event exists
						if current_event.parent is not None:
							current_event = current_event.parent # if the event has a parent, set the parent to current
						else:
							self.top_level.append(current_event) # event has no parent, it's a top-level log item
							current_event = None

				else:
					self.bad_bytes += 1

				self.pos() # update seeker position for next byte (if not EOF)

		print()
		print("finished reading, {0} bad bytes".format(self.bad_bytes))
		print()
		print("version {0}".format(self.version))
		print("timestamp {0}".format(self.timestamp))
		print("event count {0}".format(self.event_count))
		print("statement count {0}".format(self.statement_count))
		print("time: {0}".format(time.time() - s))

