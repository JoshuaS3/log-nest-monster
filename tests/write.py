#!/usr/bin/env python

import sys
import os
import time
import ctypes

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

	ts2 = ulonglong(milli())
	verbosity = uchar(0)

	tag = enc("INIT")
	tag_len = uchar(len(tag))

	message = enc("HELLO")
	message_len = ushort(len(message))

	try:
		f = open(out, "wb")

		f.write(version)
		f.write(queue_time)
		f.write(open_event)
		f.write(open_statement)
		f.write(ts2)
		f.write(verbosity)
		f.write(tag_len)
		f.write(tag)
		f.write(message_len)
		f.write(message)
		f.write(close_statement)
		f.write(close_event)
	finally:
		f.close()
		print(os.stat(out).st_size)


