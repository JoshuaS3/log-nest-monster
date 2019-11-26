// lognestmonster Copyright (c) 2019 Joshua 'joshuas3' Stockin
// main.c
// C file for testing the lognestmonster library header

// <https://github.com/JoshuaS3/lognestmonster/>.


// This file is part of lognestmonster.

// lognestmonster is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// lognestmonster is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with lognestmonster. If not, see <https://www.gnu.org/licenses/>.

#include <stdio.h>
#include "lognestmonster.h"

static char * queueName = "master";
static char * queuePath = "~/path";

int main(void) {
	long t1 = lnm_getus();

	printf("lognestmonster C test main()\n");
	printf("============================\n");
	printf("\n\n");


	printf("data testing\n");
	printf("----------------------------\n");

	printf("word size/ptr length: %li\n", sizeof(lnmItem));
	printf("\n");

	printf("enum lnmVerbosityLevel {\n");
	printf("\tlnmInfo = %d,\n\tlnmDebug = %d,\n\tlnmVerbose = %d,\n\tlnmVeryVerbose = %d,\n\tlnmWarning = %d,\n\tlnmError = %d\n}\n", lnmInfo, lnmDebug, lnmVerbose, lnmVeryVerbose, lnmWarning, lnmError);
	printf("\n\n");

	printf("core library\n");
	printf("----------------------------\n");

	printf("creating \"%s\" queue with path \"%s\"\n", queueName, queuePath);
	lnmQueue queue = lnmQueueInit(queueName, queuePath);
	printf("queue \"%s\" created at 0x%lx\n", queueName, (long)queue);
	printf("\n");

	printf("checking queue integrity in registry...\n");
	printf("queue == lnmQueueByName(\"%s\"): ", queueName);
	if (queue == lnmQueueByName(queueName)) {
		printf("true\n");
	} else {
		printf("false. exiting...\n");
		return 1;
	}
	printf("\n");

	printf("creating an E{S} logtree\n");
	lnmEventS(lnmError, "Tag / Invoker", "Test statement pushed to single event with custom tag and message");
	printf("\n");

	printf("debug registry logtree (1 top level item expected)\n");
	lnm_debug_parse_registry();
	printf("\n\n");

	printf("tests finished\n");
	printf("----------------------------\n");
	printf("time elapsed (us): %li\n", lnm_getus() - t1);

	return 0;
}