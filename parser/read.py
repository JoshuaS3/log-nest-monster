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
	pushed = [False]
	def __init__(self):
		self.parent = None
		self.pushed = [False]

class Reader:
	fd = None

	top_level = []

	current_event = None

	event_count = 0
	statement_count = 0

	total_events = 0
	total_statements = 0

	seekable = True
	file_size = 0
	position = 0

	version = 0
	timestamp = 0

	bad_bytes = 0

	filter_time_start = -1
	filter_time_end = -1
	filter_verbosity = -1
	filter_tag = -1

	update_callbacks = []

	def __init__(self, fd, seekable=True):
		self.fd = fd

		self.top_level = []

		self.current_event = None

		self.event_count = 0
		self.statement_count = 0

		self.total_events = 0
		self.total_statements = 0

		self.seekable = seekable
		self.file_size = 0
		self.position = 0

		self.version = 0
		self.timestamp = 0

		self.bad_bytes = 0

		self.filters = False

		self.filter_time_start = -1
		self.filter_time_end = -1
		self.filter_verbosity = -1
		self.filter_tag = -1

		self.update_callbacks = []

	def update(self):
		for callback in self.update_callbacks:
			callback()

	def onupdate(self, callback):
		self.update_callbacks.append(callback)

	def size(self):
		self.fd.seek(0, os.SEEK_END) # go to end of file and get position
		newsize = self.fd.tell()
		self.fd.seek(self.position) # return to previous position

		is_diff = self.file_size is not newsize
		self.file_size = newsize
		return is_diff

	def pos(self):
		p = self.fd.tell()
		self.position = p
		return p

	def seek(self, position):
		self.position = position
		self.fd.seek(self.position)

	def read(self, byte_count):
		return self.fd.read(byte_count)

	def fetch_item(self, position):
		previouspos = self.pos()
		self.seek(position)
		timestamp = ulonglong(self.read(8))
		verbosity = uchar(self.read(1))
		tag_size = uchar(self.read(1))
		tag = self.read(tag_size).decode("utf-8")
		message_size = ushort(self.read(2))
		message = self.read(message_size).decode("utf-8")
		self.seek(previouspos)
		return (timestamp, verbosity, tag, message)

	def parse_block(self, in_byte):
		seekable = self.seekable
		if in_byte == STATEMENT_START: # the byte indicates a statement's start, begin interpreting
			if seekable:
				this_position = self.pos() # identify and save the seeker position of this statement

			try:
				block = self.read(10)
				timestamp = ulonglong(block[:8])
				verbosity = block[8]
				tag = self.read(block[9])
			
				append = True

				if self.filters:
					if self.filter_time_start is not -1 and append:
						append = timestamp > self.filter_time_start

					if self.filter_time_end is not -1 and append:
						append = timestamp < self.filter_time_end

					if self.filter_verbosity is not -1 and append:
						append = verbosity in self.filter_verbosity

					if self.filter_tag is not -1 and append:
						tag = tag.decode("utf-8")
						append = tag == self.filter_tag

				message_size = ushort(self.read(2))
				if seekable:
					self.read(message_size)
					while self.read(1)[0] is not STATEMENT_END and self.pos() < self.file_size:
						self.bad_bytes += 1
				else:
					message = self.read(message_size).decode("utf-8")
					while self.read(1)[0] is not STATEMENT_END:
						self.bad_bytes += 1

				if append == True:
					self.statement_count += 1
					if self.current_event is not None:
						if seekable:
							self.current_event.pushed.append(this_position)
						else:
							self.current_event.pushed.append((timestamp, verbosity, tag, message))
					else:
						if seekable:
							self.top_level.append(this_position)
						else:
							self.top_level.append((timestamp, verbosity, tag, message))
				self.total_statements += 1
			except:
				return -1

		elif in_byte == EVENT_START: # the byte indicates an event's start, create an event
			new_event = EventProto()
			if self.current_event is not None: # we're already inside an event, set the new event's parent to match
				new_event.parent = self.current_event
			self.current_event = new_event


		elif in_byte == EVENT_END: # end of event
			if self.current_event is not None:
				if len(self.current_event.pushed) > 1:
					self.event_count += 1
					if self.current_event.parent is not None:
						self.current_event.parent.pushed.append(self.current_event)
						self.current_event = self.current_event.parent
					else:
						self.top_level.append(self.current_event)
						self.current_event = None
				else: # event is empty
					if self.current_event.parent is not None:
						self.current_event = self.current_event.parent
					else:
						self.current_event = None
				self.total_events += 1
			else:
				self.bad_bytes += 1 # event doesn't exist, bad byte
				return -1

		else: # unknown byte
			self.bad_bytes += 1
			return -1

	def scan(self): # scan for events and statements from self.position to the end of file
		if not self.seekable: raise Exception("attempting to scan non-seekable stream")
		if self.pos() == 0: # if it's the start of the file, grab version and timestamp
			self.version = self.read(1)[0]
			self.timestamp = ulonglong(self.read(8))

		while self.pos() < self.file_size: # while the seeker is before EOF
			in_byte = self.read(1)[0] # read 1 byte
			self.parse_block(in_byte) # parse block based on byte read
			self.update() # trigger callbacks

