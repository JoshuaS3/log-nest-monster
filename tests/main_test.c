// lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin (copyrighted under the MIT License)
// <https://joshstock.in>
// <https://github.com/JoshuaS3/lognestmonster>
//
// main_test.c
// Second part of a two-piece lognestmonster unit test source

#include <stdio.h>
#include "lognestmonster.h"

char * queueName;
void test(void) {
	printf("retrieving %s from global queue\n", queueName);
	lnmQueueByName(queueName);
}
