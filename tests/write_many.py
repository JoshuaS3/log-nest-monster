#!/usr/bin/env python3

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

import sys
import os
import time
import ctypes
import random

def exists(f):
	return os.path.isfile(f) or os.path.isdir(f)

def milli():
	return int(round(time.time() * 1000))

def enc(string):
	return string.encode("utf-8")

def ushort(n):
	return ctypes.c_ushort(n)

def uchar(n):
	return ctypes.c_ubyte(n)

def ulonglong(n):
	return ctypes.c_ulonglong(n)

def s(n=20):
	l = int(random.random()*n)
	st = ""
	for i in range(0, l):
		c = 97+int(random.random()*25)
		st += chr(c)
	return st

open_statement = uchar(0)
close_statement = uchar(1)
open_event = uchar(2)
close_event = uchar(3)

def output_statement(f):
	t = milli()
	ts = ulonglong(t)

	verbosity = uchar(round(random.random()*5))

	tag = enc(s(10))
	tag_len = uchar(len(tag))

	message = enc(s(20))
	message_len = ushort(len(message))
	f.write(open_statement)
	f.write(ts)
	f.write(verbosity)
	f.write(tag_len)
	f.write(tag)
	f.write(message_len)
	f.write(message)
	f.write(close_statement)

	raw = str(t) + " - INFO - " + tag.decode("utf-8") + " - " + message.decode("utf-8") + "\n"
	return len(raw)

def block(f):
	s_count = round(random.random()*8)
	for i in range(0, s_count):
		output_statement(f)
	event_chance = (random.random()*8) > 6
	if event_chance:
		f.write(open_event)
		block(f)
		f.write(close_event)

if __name__ == "__main__":
	try:
		out = sys.argv[1]
	except:
		print("must provide an out location")
		exit(1)

	try:
		count = int(sys.argv[2])
	except:
		print("must provide a loop count")
		exit(1)

	version = uchar(1)
	queue_time = ulonglong(milli())

	start = milli()

	try:
		f = open(out, "wb")

		f.write(version)
		f.write(queue_time)

		for i in range(0, count):
			print("{0}%".format(round((i/count)*1000)/10), end="\r")
			block(f)


	finally:
		f.close()
		size = os.stat(out).st_size
		print("file written with size {0}MB in {1} seconds".format(round(size/1000)/1000, (milli()-start)/1000))


