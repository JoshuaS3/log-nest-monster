#!/usr/bin/env python

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
	return string.encode("latin-1")

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
		c = 97+int(random.random()*26)
		st += chr(c)
	return st

if __name__ == "__main__":
	try:
		out = sys.argv[1]
	except:
		print("must provide an out location")
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
		for i in range(0, 50000):
			ts = ulonglong(milli())

			tag = enc("hello")#enc(s(10))
			tag_len = uchar(len(tag))

			message = enc(s(100))
			message_len = ushort(len(message))
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
		print("file written with size {0} in {1} seconds".format(os.stat(out).st_size, (milli()-start)/1000))


