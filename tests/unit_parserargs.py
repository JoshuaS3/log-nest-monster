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

import time
import subprocess

def call(command):
	command = command.split()
	popen = subprocess.Popen(command, stdout=subprocess.PIPE)
	try:
		code = popen.wait(5)
		message = popen.stdout.read().decode("utf-8").strip()
	except:
		code = 2
		message = "timeout or other error"
	return (code, message)

commands = [
	("", 0),
	("--help", 0),
	("--version", 0),
	("--asdf", 1),
	("--after 10", 0),
	("--after 10 0", 1),
	("--after string", 1),
	("--before", 1),
	("--before 10", 0),
	("--before 10 0", 1),
	("--before string", 1),
	("--status", 1),
	("-i", 0),
	("-e", 0),
	("-i -e", 0),
	("-i -e -d -v -vv", 0),
	("-i -e 1 3 -d -v -vv", 1),
	("-i -e -d 14 -v -vv 6", 1),
	("-i 92 -e -d -v 139812479812 983 afiow ;a3r -vv", 1),
	("random arg u m ents", 1),
	("--tag", 1),
	("--tag 17", 0)
]

if __name__ == "__main__":
	exitcode = 0
	start = time.time()
	print("Beginning argument testing")
	print()
	for command in commands:
		val = "bash ./lognestmonster --status " + command[0] + " bin/w2.lnm"
		response = call(val)
		print(str(command[1]) + ": " + val)
		if response[0] is not command[1]: # if response codes don't match up
			print("[[ERROR: expected response code " + str(command[1]) + ", got " + str(response[0]) + "]]")
			print("---------- OUTPUT BEGIN ----------")
			print(response[1])
			print("----------- OUTPUT END -----------")
			print()
			exitcode = 1
	print()
	print("Finished argument testing with overall exit code " + str(exitcode))
	exit(exitcode)
