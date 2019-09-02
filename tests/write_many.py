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

if __name__ == "__main__":
	try:
		out = sys.argv[1]
	except:
		print("must provide an out location")
		exit(1)

	try:
		count = int(sys.argv[2])
	except:
		print("must provide a statement count")
		exit(1)

	version = uchar(1)
	queue_time = ulonglong(milli())
	open_statement = uchar(0)
	close_statement = uchar(1)
	open_event = uchar(2)
	close_event = uchar(3)

	verbosity = uchar(0)

	start = milli()

	try:
		f = open(out, "wb")

		f.write(version)
		f.write(queue_time)

		f.write(open_event)
		for i in range(0, count):
			print("{0}%".format(round((i/count)*1000)/10), end="\r")
			ts = ulonglong(milli())

			tag = enc(s(10))
			tag_len = uchar(len(tag))

			message = enc(s(20))
			message_len = ushort(len(message)+1)
			f.write(open_statement)
			f.write(ts)
			f.write(verbosity)
			f.write(tag_len)
			f.write(tag)
			f.write(message_len)
			f.write(message)
			f.write(close_statement)
		f.write(close_event)

	finally:
		f.close()
		print("file written with size {0}MB in {1} seconds".format(round(os.stat(out).st_size/1000)/1000, (milli()-start)/1000))


