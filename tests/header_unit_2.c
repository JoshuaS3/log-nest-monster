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

// main_test.c
// Second part of the main lognestmonster unit test. Tests queue integrity
// across translation units.

#include <stdio.h>   // printf
#include <stdlib.h>  // abort
#include "lognestmonster.h"

void verify_queue_integrity(lnmQueue queue, char * queueName) {
	printf("tests/header_unit_2.c: queue == lnmQueueByName(\"%s\"): ", queueName);
	if (queue == lnmQueueByName(queueName)) {
		printf("true\n");
	} else {
		printf("false. exiting...\n");
		abort();
	}
}
