/* lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin
 * <https://joshstock.in>
 * <https://github.com/JoshuaS3/lognestmonster>
 *
 * This software is licensed and distributed under the terms of the MIT License.
 * See the MIT License in the LICENSE file of this project's root folder.
 *
 * This comment block and its contents, including this disclaimer, MUST be
 * preserved in all copies or distributions of this software's source.
 */

// parser/main.c
// Entry point for the CLI parser program. Parses input arguments and handles
// component initialization and configuration.


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <curses.h>


int main(int argc, char * argv[]) {
	for (int iter = 1; iter < argc; iter++) {
		char * arg = argv[iter];
		if (strcmp(arg, "--help") == 0 || strcmp(arg, "-h") == 0 || strcmp(arg, "-?") == 0) {
			printf("usage: lognestmonster [--help | -h | -?] [--version | -v]\n");
			exit(0);
		} else if (strcmp(arg, "--version") == 0 || strcmp(arg, "-v") == 0) {
			printf("lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin\n");
			printf("<https://joshstock.in> <https://github.com/JoshuaS3/lognestmonster>\n");
			printf("This software's source is licensed and distributed under the terms of the MIT License.\n");
			exit(0);
		} else {
			printf("lognestmonster (parser/main): unknown argument \"%s\", exiting...\n", arg);
			exit(1);
		}
	}

	initscr();
	noecho();

	attron(A_BOLD | A_STANDOUT);
	mvaddstr(10, 0, "lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin");
	attroff(A_BOLD | A_STANDOUT);
	refresh();

	while (1) {
		char ch = getch();
		if (ch == 'q' || ch == 'Q') break;
	}

	endwin();

	return 0;
}
