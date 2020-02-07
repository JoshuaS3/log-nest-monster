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

// main.c
// C file for testing the lognestmonster library header

#include <stdio.h>

#define LNM_INIT
#define LNM_DEBUG
#include "lognestmonster.h"

void verify_queue_integrity(lnmQueue queue, char * queueName);

int main(void) {
	long t1 = lnm_getus();

	printf("data testing\n");
	printf("============\n");

	printf("word size/ptr length: %zu\n", sizeof(lnmItem));
	printf("\n\n");

	printf("queue persistence testing\n");
	printf("=========================\n");

	printf("creating \"master\" queue with path \"/var/log/lognestmonster\"\n");
	lnmQueue queue = lnmQueueInit("master", "/var/log/lognestmonster");
	printf("queue \"master\" created at 0x%llx\n", (long long)queue);
	printf("\n");

	printf("checking queue integrity in registry...\n");
	printf("tests/header_unit.c: queue == lnmQueueByName(\"master\"): ");
	if (queue == lnmQueueByName("master")) {
		printf("true\n");
	} else {
		printf("false. exiting...\n");
		return 1;
	}
	printf("checking queue integrity across translation units...\n");
	verify_queue_integrity(queue, "master");
	printf("\n\n");

	printf("log tree persistence testing\n");
	printf("============================\n");

	printf("creating log tree\n");
	lnmItem event = lnmEvent("EVENT_TAG");
	lnmEventPushS(event, lnmInfo, "Each log statement has a verbosity level attached and holds general information you want to write in a log file.");
	lnmEventPushS(event, lnmVerbose, "There are 6 verbosity levels: lnmInfo, lnmDebug, lnmVerbose, lnmVeryVerbose, lnmWarning, and lnmError.");
	lnmEventPushS(event, lnmInfo, "An event is a container for log statements or other events. Events can later be deserialized and queried.");
	lnmEventPushS(event, lnmVeryVerbose, "Events can hold other events, like this: ");
	lnmItem nested_event = lnmEvent("NESTED_EVENT");
	lnmEventPush(event, nested_event);
	lnmEventPushS(nested_event, lnmDebug, "Each event is assigned a tag to make querying easy.");
	lnmEventPushS(nested_event, lnmWarning, "Events can hold up to 2^16 (65536) items. Messages also have a 2^16 maximum message length.");
	printf("created log tree\n");
	printf("\n\n");

	printf("debug registry logtree (1 top level items expected)\n");
	lnm_debug_parse_registry();
	printf("\n\n");

	printf("push event to queue\n");
	lnmQueuePush(queue, event);
	printf("\n");

	printf("debug registry logtree (0 top level items expected)\n");
	lnm_debug_parse_registry();
	printf("\n");

	printf("debug queue (master)\n");
	lnm_debug_parse_queue(queue);
	printf("\n\n");

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
