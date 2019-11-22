// lognestmonster Copyright (c) 2019 Joshua 'joshuas3' Stockin
// lognestmonster.h
// C header file for implementation of the lognestmonster logging library

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

#ifndef __LOGNESTMONSTER__
#define __LOGNESTMONSTER__ 1

// SEMANTICS
// internal definitions: lnm_lower_camel_case
// public definitions:   lnmUpperCamelCase

// stdc inclusions

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>


// Base definitions

enum lnmVerbosityLevel {lnmInfo, lnmDebug, lnmVerbose, lnmVeryVerbose, lnmWarning, lnmError};
typedef uint8_t * lnmItem;
typedef uint8_t * lnmQueue;


// Pushable structure

typedef struct {
	uint16_t length;
	lnmItem * pushed;
} lnm_pushable;

lnm_pushable * lnm_new_pushable() {
	lnm_pushable * new_pushable = malloc(sizeof(lnm_pushable));
	new_pushable->length = 0;
	new_pushable->pushed = malloc(0);
	return new_pushable;
}

void lnm_pushable_push(lnm_pushable * pushable, lnmItem item) {
	if (pushable->length+1 >= 65535) {
		printf("lognestmonster (lnm_pushable_push): pushable reached cap length 65535. exiting...\n");
		exit(1);
	}
	pushable->pushed = realloc(pushable->pushed, sizeof(lnmItem)*(pushable->length+1)); // reallocate with size: length+1
	pushable->pushed[pushable->length] = item;
	pushable->length += 1;
}

int lnm_pushable_indexof(lnm_pushable * pushable, lnmItem item) {
	int len = pushable->length;
	for (int iter = 0; iter<len; iter++) {
		if (item == pushable->pushed[iter]) return iter;
	}
	return -1;
}

void lnm_pushable_remove(lnm_pushable * pushable, int index) {
	if (index>=pushable->length || index < 0) {
		printf("lognestmonster (lnm_pushable_remove): attempt to remove index out of pushable bounds. exiting...\n");
		exit(1);
	}
	lnmItem * new_pushed = malloc(sizeof(lnmItem)*(pushable->length-1)); // map array excluding index
	for (int iter = 0; iter<index; iter++) {
		new_pushed[iter] = pushable->pushed[iter];
	}
	for (int iter = index+1; iter<pushable->length; iter++) {
		new_pushed[iter-1] = pushable->pushed[iter];
	}
	free(pushable->pushed);
	pushable->length--;
	pushable->pushed = new_pushed;
}


// Statement and event structure definitions

typedef struct {
	uint8_t        type:1; // Used internally; 0 = statement, 1 = event
	lnm_pushable * pushed; // array of memory locations for lnm_log_event and lnm_log_statement structs
} lnm_log_event;

typedef struct {
	// word 1, 4 bytes data 4 bytes padding
	uint8_t  type:1;       // Used internally; 0 = statement, 1 = event
	uint8_t  verbosity:3;  // lnmVerbosityLevel, 0-5
	uint8_t  tag_size;     // character length of the tag
	uint16_t message_size; // character length of the message

	// word 2, 8 bytes data
	uint64_t timestamp;    // 64-bit millisecond timestamp

	// word 3, 8 bytes data
	char *   log;          // tag string + message string
} lnm_log_statement;


// Queue structure definition

typedef struct {
	char * name;
	char * out_path;
	uint64_t timestamp;
	lnm_pushable * pushed;
} lnm_queue;


// Library utilities

unsigned long lnm_getus(void) {
	struct timeval current_time;
	gettimeofday(&current_time, NULL);
	unsigned long ms = (current_time.tv_sec*1000000+current_time.tv_usec);
	return ms;
}

unsigned long lnm_getms(void) {
	return lnm_getus()/1000;
}


int lnm_isstatement(lnmItem item) {
	lnm_log_statement * s = (lnm_log_statement *)item;
	return !s->type;
}


// Item registry utils

lnm_pushable * registered_queues;
lnm_pushable * registered_items;

int lnm_treescan_match(lnmItem toscan, lnmItem match) {

}

void lnm_registry_update(void) { // scan each registered item

}


// Core library

lnmQueue lnmQueueInit(char * name, char * out_path) {
	if (registered_queues == NULL) {
		registered_queues = lnm_new_pushable();
	}
	if (registered_items == NULL) {
		registered_items = lnm_new_pushable();
	}

	lnm_queue * new_queue = malloc(sizeof(lnm_queue));
	new_queue->name = malloc(strlen(name)+1);
	new_queue->out_path = malloc(strlen(out_path)+1);
	strcpy(new_queue->name, name);
	strcpy(new_queue->out_path, out_path);
	new_queue->pushed = lnm_new_pushable();

	lnm_pushable_push(registered_queues, (lnmQueue)new_queue);
	return (lnmQueue)new_queue;
}

lnmQueue lnmQueueByName(char * name) {
	if (registered_queues == NULL) {
		printf("lognestmonster (lnmQueueByName): queue registry is nonexistant. exiting...\n");
		exit(1);
	}
	if (registered_queues->length == 0) {
		printf("lognestmonster (lnmQueueByName): queue registry is empty. exiting...\n");
		exit(1);
	}
	for (int iter = 0; iter<registered_queues->length; iter++) {
		lnm_queue * iterqueue = (lnm_queue *)registered_queues->pushed[iter];
		if (strcmp(iterqueue->name, name)==0) {
			return (lnmQueue)iterqueue;
		}
	}
	printf("lognestmonster (lnmQueueByName): queue not found in registry. exiting...\n");
	exit(1);
}


lnmItem lnmStatement(uint8_t verbosity, char * tag, char * message) {
	lnm_log_statement * new_statement = malloc(sizeof(lnm_log_statement));
	new_statement->type = 0;
	new_statement->verbosity = verbosity;
	new_statement->timestamp = lnm_getms();
	int tlen = strlen(tag);
	if (tlen > 255 || tlen < 0) {
		printf("lognestmonster (lnmStatement): tag length %i is longer than the cap 255 characters. exiting...\n", tlen);
		exit(1);
	}
	int mlen = strlen(message);
	if (mlen > 65535 || mlen < 0) {
		printf("lognestmonster (lnmStatement): message length %i is longer than the cap 65535 characters. exiting...\n", mlen);
		exit(1);
	}
	new_statement->tag_size = tlen;
	new_statement->message_size = mlen;
	new_statement->log = malloc(tlen+mlen+1);
	strcpy(new_statement->log, tag);
	strcat(new_statement->log, message);
	return (lnmItem)new_statement;
}


lnmItem lnmEvent(void) {
	lnm_log_event * new_event = malloc(sizeof(lnm_log_event));
	new_event->type = 1;
	new_event->pushed = lnm_new_pushable();
	return (lnmItem)new_event;
}

void lnmEventPush(lnmItem event, lnmItem item) {
	if (event == item) {
		printf("lognestmonster (lnmEventPush): attempt to push event to self. exiting...\n");
		exit(1);
	}
	lnm_log_event * event_t = (lnm_log_event *)event;
	if (event_t->type != 1) {
		printf("lognestmonster (lnmEventPush): cannot cast non-event to event type. exiting...\n");
		exit(1);
	}
	lnm_pushable_push(event_t->pushed, item);
}

void lnmEventPushS(lnmItem event, uint8_t verbosity, char * tag, char * message) {
	lnmItem statement = lnmStatement(verbosity, tag, message);
	lnmEventPush(event, statement);
}

lnmItem lnmEventI(lnmItem item) {
	lnmItem event = lnmEvent();
	lnmEventPush(event, item);
	return event;
}

lnmItem lnmEventS(uint8_t verbosity, char * tag, char * message) {
	lnmItem statement = lnmStatement(verbosity, tag, message);
	return lnmEventI(statement);
}


void lnm_debug_tabs(int count) {
	for (int i = 0; i < count; i++) {
		printf("  ");
	}
}

void lnm_debug_parse(lnmItem item, int tabcount) {
	if (lnm_isstatement(item)) {
		lnm_log_statement * statement = (lnm_log_statement *) item;
		lnm_debug_tabs(tabcount);
		printf("Statement {\n");

		lnm_debug_tabs(tabcount+1);
		char * verbosity;
		switch (statement->verbosity) {
			case 0:
				verbosity = "INFO";
				break;
			case 1:
				verbosity = "DEBUG";
				break;
			case 2:
				verbosity = "VERBOSE";
				break;
			case 3:
				verbosity = "VERYVERBOSE";
				break;
			case 4:
				verbosity = "WARNING";
				break;
			case 5:
				verbosity = "ERROR";
				break;
		}
		printf("Verbosity %s\n", verbosity);

		lnm_debug_tabs(tabcount+1);
		printf("Timestamp %ld\n", statement->timestamp);

		lnm_debug_tabs(tabcount+1);
		char tag[statement->tag_size+1];
		strncpy(tag, statement->log, statement->tag_size);
		tag[statement->tag_size] = '\0';
		printf("Tag (%i) %s\n", statement->tag_size, tag);

		lnm_debug_tabs(tabcount+1);
		char message[statement->message_size+1];
		strncpy(message, statement->log+statement->tag_size, statement->message_size);
		message[statement->message_size] = '\0';
		printf("Message (%i) %s\n", statement->message_size, message);

		lnm_debug_tabs(tabcount);
		printf("}\n");
	} else if (!lnm_isstatement(item)) {
		lnm_log_event * event = (lnm_log_event *) item;
		lnm_debug_tabs(tabcount);
		printf("Event (%i) [\n", event->pushed->length);
		for (int i = 0; i < event->pushed->length; i++) {
			lnmItem item = event->pushed->pushed[i];
			lnm_debug_parse(item, tabcount + 1);
		}
		lnm_debug_tabs(tabcount);
		printf("]\n");
	} else {
		printf("lognestmonster (lnm_debug_parse): unknown item type. exiting...\n");
		exit(1);
	}
}

#endif
