# get character from stdin

import termios, sys, tty
def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


# echo output

import subprocess
def output(*array):
	s = "".join(array)
	a=subprocess.run(["echo", "-e", s]);


# ANSI codes for output

RESET = "\e[0m"
BOLD = "\e[1m"
UNDERLINED = "\e[4m"
CONTRAST = "\e[7m"

TEXT_RED = "\e[91m"
TEXT_GREEN = "\e[92m"
TEXT_YELLOW = "\e[93m"
TEXT_MAGENTA = "\e[95m"
TEXT_CYAN = "\e[96m"

BACK_RED = "\e[101m"
BACK_GREEN = "\e[102m"
BACK_YELLOW = "\e[103m"
BACK_MAGENTA = "\e[105m"
BACK_CYAN = "\e[106m"
