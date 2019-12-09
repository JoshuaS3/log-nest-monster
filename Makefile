.phony: all tests c_unit clean

all: tests
tests: c_unit

c_unit:
	gcc -o bin/c tests/main.c tests/main_test.c -Wall -Wextra -Werror -pedantic -I"./src/c"

clean:
	rm -rf bin/*
	rmdir bin/
