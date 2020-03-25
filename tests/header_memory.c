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

// header_memory.c
// Test memory usage on lognestmonster library to prevent leaks

#include <stdio.h>
#include <sys/resource.h>

#define LNM_INIT
#define LNM_ALL
#define LNM_DEBUG
#include "lognestmonster.h"

int main() {
	long t1 = lnm_getus();

	struct rusage r_usage;
	getrusage(RUSAGE_SELF, &r_usage);
	printf("Memory usage before: %li\n", r_usage.ru_maxrss);

	lnmItem lastEvent = NULL;
	for (int iter = 0; iter < 1000; iter++) {
		uint64_t time = lnm_getus();
		int type = time % 5 == 0 ? LNM_EVENT : LNM_STATEMENT;
		if (type == LNM_STATEMENT) {
			char message[25];
			snprintf(message, 25, "New statement #%i", iter);
			if (lastEvent == NULL) {
				lnmStatement(lnmInfo, message);
			} else {
				lnmEventPushS(lastEvent, lnmInfo, message);
			}
		} else if (type == LNM_EVENT) {
			char tag[20];
			snprintf(tag, 20, "New event #%i", iter);
			if (lastEvent == NULL || time % 7 == 0) {
				lastEvent = lnmEvent(tag);
			} else {
				lnmItem new_event = lnmEvent(tag);
				lnmEventPush(lastEvent, new_event);
				lastEvent = new_event;
			}
		}
	}

	lnm_debug_parse_registry();

	getrusage(RUSAGE_SELF, &r_usage);
	printf("Memory usage during test: %li\n", r_usage.ru_maxrss);

	lnm_registry_free();
	lnm_debug_parse_registry();

	getrusage(RUSAGE_SELF, &r_usage);
	printf("Memory usage after: %li\n", r_usage.ru_maxrss);

	printf("time elapsed (us): %lu\n", lnm_getus() - t1);
	return 0;
}
