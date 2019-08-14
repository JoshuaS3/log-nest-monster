#!/usr/bin/env python3

from utils import *
from text import *

def input_loop():
	while True:
		input = getch().lower()
		if input == "q":
			break;

if __name__ == "__main__":
	output(version_message)
