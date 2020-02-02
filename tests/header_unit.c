// lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin
// <https://joshstock.in>
// <https://github.com/JoshuaS3/lognestmonster>
// This software is licensed under the MIT License.
//
// main.c
// C file for testing the lognestmonster library header

#include <stdio.h>

#define LNM_INIT
#define LNM_ALL
#include "lognestmonster.h"

void test(void);
extern char * queueName;
static char * queuePath = "~/path";

int main(void) {
	queueName = "master";
	long t1 = lnm_getus();

	printf("lognestmonster C test main()\n");
	printf("============================\n");
	printf("\n\n");


	printf("data testing\n");
	printf("----------------------------\n");

	printf("word size/ptr length: %li\n", sizeof(lnmItem));
	printf("\n");

	printf("enum lnmVerbosityLevel {\n");
	printf("\tlnmInfo = %i,\n\tlnmDebug = %i,\n\tlnmVerbose = %i,\n\tlnmVeryVerbose = %i,\n\tlnmWarning = %i,\n\tlnmError = %i\n}\n", lnmInfo, lnmDebug, lnmVerbose, lnmVeryVerbose, lnmWarning, lnmError);
	printf("\n\n");

	printf("core library\n");
	printf("----------------------------\n");

	printf("creating \"%s\" queue with path \"%s\"\n", queueName, queuePath);
	lnmQueue queue = lnmQueueInit(queueName, queuePath);
	printf("queue \"%s\" created at 0x%llx\n", queueName, (long long)queue);
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

	printf("creating an E{2S, E{1S}, 1S} logtree\n");
	lnmItem event = lnmEventS(lnmError, "INVOKER", "Test ERROR statement pushed to single event with custom tag and message");
	lnmEventPushS(event, lnmInfo, "INIT", "Sample INFO/INIT log statement");

	lnmItem event2 = lnmEventS(lnmVerbose, "NESTED", "Example of a nested log statement");
	lnmEventPushS(event2, lnmVeryVerbose, "NESTED", "Nested #2");

	lnmEventPush(event, event2);

	lnmEventPushS(event2, lnmInfo, "TEST", "Item #3");
	lnmEventPushS(event2, lnmInfo, "TEST", "Item #4");

	lnmItem event3 = lnmEventS(lnmWarning, "NESTED-2", "Third layer log statement");
	lnmEventPush(event2, event3);

	lnmEventPushS(event2, lnmInfo, "TEST", "Item #6");
	lnmEventPushS(event2, lnmInfo, "TEST", "Item #7");
	lnmEventPushS(event2, lnmInfo, "TEST", "Item #8");
	lnmEventPushS(event2, lnmInfo, "TEST", "Item #9 (frame capacity doubles from 8 to 16)");

	lnmEventPushS(event, lnmDebug, "REQUEST", "DEBUG/REQUEST log statement. might be found useful in a webserver backend");
	printf("\n");

	printf("debug registry logtree (1 top level items expected)\n");
	lnm_debug_parse_registry();
	printf("\n");

	printf("push event to queue\n");
	lnmQueuePush(queue, event);
	printf("\n");

	printf("debug queue (master)\n");
	lnm_debug_parse_queue(queue);
	printf("\n");

	printf("debug registry logtree (0 top level items expected)\n");
	lnm_debug_parse_registry();
	printf("\n");

	printf("calling test function from different source file\n");
	test();
	printf("\n");

	printf("freeing queue\n");
	lnm_free_queue(queue);
	printf("\n");

	printf("debug queue (master, 0 items expected)\n");
	lnm_debug_parse_queue(queue);
	printf("\n\n");

	printf("tests finished\n");
	printf("----------------------------\n");
	printf("time elapsed (us): %lu\n", lnm_getus() - t1);

	return 0;
}
