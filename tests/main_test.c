// lognestmonster Copyright (c) 2019 Joshua 'joshuas3' Stockin
// main_test.c
// Second part of a two-piece lognestmonster test source

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

char * queueName;
void test(void) {
	printf("retrieving %s from global queue\n", queueName);
	lnmQueueByName(queueName);
}
