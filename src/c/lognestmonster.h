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


// SEMANTICS
// internal definitions: lnm_lower_camel_case
// public definitions:   lnmUpperCamelCase


#ifdef __cplusplus // Linker protection
extern "C" {
#endif

// Declarations
#ifndef LOGNESTMONSTER_H
#define LOGNESTMONSTER_H 1

// stdc inclusions

#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// non-universal inclusions

#include <sys/time.h>


enum lnmVerbosityLevel {lnmInfo, lnmDebug, lnmVerbose, lnmVeryVerbose, lnmWarning, lnmError};
typedef uint8_t * lnmItem;
typedef uint8_t * lnmQueue;

lnmQueue lnmQueueInit(char * name, char * out_path);
lnmQueue lnmQueueByName(char * name);
lnmItem lnmStatement(enum lnmVerbosityLevel verbosity, char * tag, char * message);
lnmItem lnmEvent(void);
void lnmEventPush(lnmItem event, lnmItem item);
void lnmEventPushS(lnmItem event, uint8_t verbosity, char * tag, char * message);
lnmItem lnmEventI(lnmItem item);
lnmItem lnmEventS(uint8_t verbosity, char * tag, char * message);

#ifdef LNM_ALL // Exposes the private API declarations

// Pushable utilities
typedef struct lnm_pushable lnm_pushable;

void lnm_pushable_realloc(lnm_pushable * pushable);
lnm_pushable * lnm_new_pushable(void);
void lnm_pushable_push(lnm_pushable * pushable, lnmItem item);
int lnm_pushable_indexof(lnm_pushable * pushable, lnmItem item);
void lnm_pushable_pop(lnm_pushable * pushable);
void lnm_pushable_remove(lnm_pushable * pushable, uint32_t index);
void lnm_pushable_free(lnm_pushable * pushable);

// Log item and object struct types
typedef struct lnm_log_event lnm_log_event;
typedef struct lnm_log_statement lnm_log_statement;
typedef struct lnm_queue lnm_queue;

// General utilities
unsigned long lnm_getus(void);
unsigned long lnm_getms(void);
int lnm_isstatement(lnmItem item);

// Registry utilities
void lnm_registry_update(void);

// Memory utilities
void lnm_free_item(lnmItem item);
void lnm_free_registry(void);
void lnm_free_queue(lnmQueue queue);

// Debug utilities
void lnm_debug_tabs(int count);
void lnm_debug_parse_item(lnmItem item, int tabcount);
void lnm_debug_parse_registry(void);
void lnm_debug_parse_queue(lnmQueue queue);

#endif // LNM_ALL, private declarations
#endif // LOGNESTMONSTER_H, public declarations


#ifdef LNM_INIT // one-time definitions


// Pushable structure

typedef struct lnm_pushable {
	uint32_t capacity;
	uint32_t length;
	lnmItem * pushed;
} lnm_pushable;

void lnm_pushable_realloc(lnm_pushable * pushable) {
	if (pushable->length > pushable->capacity) {
		if (pushable->capacity * 2 <= pushable->capacity) {
			printf("lognestmonster (lnm_pushable_realloc): pushable reached max length of 2^32-1. exiting...\n");
			exit(1);
		}
		pushable->pushed = realloc(pushable->pushed, sizeof(lnmItem) * (pushable->capacity *= 2));
	} else if (pushable->length < (pushable->capacity / 2)) {
		if (pushable->capacity > 8) {
			pushable->pushed = realloc(pushable->pushed, sizeof(lnmItem) * (pushable->capacity /= 2));
		}
	}
}

lnm_pushable * lnm_new_pushable(void) {
	lnm_pushable * new_pushable = malloc(sizeof(lnm_pushable));
	new_pushable->capacity = 8;
	new_pushable->length = 0;
	new_pushable->pushed = malloc(sizeof(lnmItem)*new_pushable->capacity);
	return new_pushable;
}

void lnm_pushable_push(lnm_pushable * pushable, lnmItem item) {
	pushable->length++;
	lnm_pushable_realloc(pushable);
	pushable->pushed[pushable->length-1] = item;
}

int lnm_pushable_indexof(lnm_pushable * pushable, lnmItem item) {
	int len = pushable->length;
	for (int iter = 0; iter<len; iter++) {
		if (item == pushable->pushed[iter]) return iter;
	}
	printf("lognestmonster (lnm_pushable_indexof): cannot find item in pushable. exiting...\n");
	exit(1);
}

void lnm_pushable_pop(lnm_pushable * pushable) {
	pushable->length--;
	lnm_pushable_realloc(pushable);
}

void lnm_pushable_remove(lnm_pushable * pushable, uint32_t index) {
	if (index>=pushable->length) {
		printf("lognestmonster (lnm_pushable_remove): attempt to remove index out of pushable bounds. exiting...\n");
		exit(1);
	}
	for (uint32_t iter = index; iter<pushable->length-1; iter++) {
		pushable->pushed[iter] = pushable->pushed[iter+1];
	}
	pushable->length--;
	lnm_pushable_realloc(pushable);
}

void lnm_pushable_free(lnm_pushable * pushable) {
	free(pushable->pushed);
	free(pushable);
}


// Statement and event structure definitions

typedef struct lnm_log_event {
	// word 1, 1 byte data 7 bytes padding
	uint8_t        type:1;       // Used internally; 0 = statement, 1 = event
	uint8_t        boolpushed:1; // whether or not this log item has been pushed
	uint8_t        verbosity:3;  // lnmVerbosityLevel, 0-5

	// word 2, 8 bytes data
	char *         tag;          // tag string

	// word 3, 8 bytes data
	lnm_pushable * pushed;       // array of memory locations for lnm_log_event and lnm_log_statement structs
} lnm_log_event;

typedef struct lnm_log_statement {
	// word 1, 4 bytes data 4 bytes padding
	uint8_t  type:1;       // Used internally; 0 = statement, 1 = event
	uint8_t  boolpushed:1; // whether or not this log item has been pushed
	uint8_t  verbosity:3;  // lnmVerbosityLevel, 0-5
	uint8_t  tag_size;     // character length of the tag
	uint16_t message_size; // character length of the message

	// word 2, 8 bytes data
	uint64_t timestamp;    // 64-bit millisecond timestamp

	// word 3, 8 bytes data
	char *   log;          // tag string + message string
} lnm_log_statement;


// Queue structure definition

typedef struct lnm_queue {
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

static lnm_pushable * lnm_registered_queues;
static lnm_pushable * lnm_registered_items;
static int lnm_registry_update_count;

void lnm_registry_update(void) { // scan each registered item
	for (uint32_t iter = 0; iter < lnm_registered_items->length; iter++) {
		lnm_log_statement * s = (lnm_log_statement *)lnm_registered_items->pushed[iter];
		if (s->boolpushed == 1) { // if the registered item has been pushed elsewhere, remove it from the top level of the registry
			lnm_registry_update_count++;
			lnm_pushable_remove(lnm_registered_items, iter);
			iter--;
		}
	}
}


// Core library

void lnm_free_item(lnmItem item) {
	lnm_log_statement * item_cast = (lnm_log_statement *)item;
	if (item_cast->boolpushed == 0) { // flush item out of registry
		item_cast->boolpushed = 1;
		lnm_registry_update();
	}
	if (item_cast->type == 0) {
		free(item_cast->log);
		free(item_cast);
	} else if (item_cast->type == 1) {
		lnm_log_event * event_cast = (lnm_log_event *)item_cast;

		lnm_pushable * breadcrumb = lnm_new_pushable();
		lnm_pushable_push(breadcrumb, (lnmItem)event_cast); // add event_cast as the first step down the breadcrumb
		while (breadcrumb->length > 0) {                    // while there are items still in the breadcrumb
			lnm_log_statement * breadcrumb_item = (lnm_log_statement *)breadcrumb->pushed[breadcrumb->length-1]; // fetch the last (deepest) item
			if (breadcrumb_item->type == 0) { // the item is a statement
				lnm_pushable_pop(breadcrumb); // remove it from the breadcrumb
				free(breadcrumb_item->log);   // and free it
				free(breadcrumb_item);
			} else if (breadcrumb_item->type == 1) {
				lnm_log_event * breadcrumb_item_cast = (lnm_log_event *)breadcrumb_item; // item is an event, cast pointer
				if (breadcrumb_item_cast->pushed->length > 0) {                          // if the event is not empty
					lnm_pushable_push(breadcrumb, breadcrumb_item_cast->pushed->pushed[breadcrumb_item_cast->pushed->length-1]); // push the last item of event into the breadcrumb
					lnm_pushable_pop(breadcrumb_item_cast->pushed); // and remove it from this event's index
					// there is now a new breadcrumb navigation layer. loop back to check the new item...
				} else {
					lnm_pushable_pop(breadcrumb); // event is finally empty, remove it from the breadcrumb and free it
					lnm_pushable_free(breadcrumb_item_cast->pushed);
					free(breadcrumb_item_cast);
				}
			}
		}
	} else {
		printf("lognestmonster (lnm_free_item): non-log item passed to function. exiting...\n");
		exit(1);
	}
}

void lnm_free_registry() {
	for (uint32_t iter = 0; iter < lnm_registered_items->length; iter++) {
		lnm_free_item(lnm_registered_items->pushed[iter]);
	}
}

void lnm_free_queue(lnmQueue queue) {
	lnm_queue * queue_cast = (lnm_queue *)queue;
	for (uint32_t iter = 0; iter < queue_cast->pushed->length; iter++) {
		lnm_free_item(queue_cast->pushed->pushed[iter]);
		lnm_pushable_remove(queue_cast->pushed, iter--);
	}
}


lnmQueue lnmQueueInit(char * name, char * out_path) {
	if (lnm_registered_queues == NULL) {
		lnm_registered_queues = lnm_new_pushable();
	}
	if (lnm_registered_items == NULL) {
		lnm_registered_items = lnm_new_pushable();
	}

	lnm_queue * new_queue = malloc(sizeof(lnm_queue));
	new_queue->name = malloc(strlen(name)+1);
	new_queue->out_path = malloc(strlen(out_path)+1);
	strcpy(new_queue->name, name);
	strcpy(new_queue->out_path, out_path);
	new_queue->timestamp = lnm_getus();
	new_queue->pushed = lnm_new_pushable();

	lnm_pushable_push(lnm_registered_queues, (lnmQueue)new_queue);
	return (lnmQueue)new_queue;
}

lnmQueue lnmQueueByName(char * name) {
	if (lnm_registered_queues == NULL) {
		printf("lognestmonster (lnmQueueByName): queue registry is nonexistant. exiting...\n");
		exit(1);
	}
	if (lnm_registered_queues->length == 0) {
		printf("lognestmonster (lnmQueueByName): queue registry is empty. exiting...\n");
		exit(1);
	}
	for (uint32_t iter = 0; iter<lnm_registered_queues->length; iter++) {
		lnm_queue * iterqueue = (lnm_queue *)lnm_registered_queues->pushed[iter];
		if (strcmp(iterqueue->name, name)==0) {
			return (lnmQueue)iterqueue;
		}
	}
	printf("lognestmonster (lnmQueueByName): queue not found in registry. exiting...\n");
	exit(1);
}

void lnmQueuePush(lnmQueue queue, lnmItem item) {
	if (((lnm_log_statement *)item)->boolpushed == 1) {
		printf("lognestmonster (lnmQueuePush): attempt to push an already-pushed log item. exiting...\n");
		exit(1);
	}
	lnm_pushable_push(((lnm_queue *)queue)->pushed, item);
	((lnm_log_statement *)item)->boolpushed = 1;
	lnm_registry_update();
}


lnmItem lnmStatement(enum lnmVerbosityLevel verbosity, char * tag, char * message) {
	lnm_log_statement * new_statement = malloc(sizeof(lnm_log_statement));
	new_statement->type = 0;
	new_statement->verbosity = verbosity;
	new_statement->timestamp = lnm_getus();
	int tlen = strlen(tag);
	if (tlen > 256 || tlen < 0) {
		printf("lognestmonster (lnmStatement): tag length %i is longer than the cap 256 characters. exiting...\n", tlen);
		exit(1);
	}
	int mlen = strlen(message);
	if (mlen > 65536 || mlen < 0) {
		printf("lognestmonster (lnmStatement): message length %i is longer than the cap 65536 characters. exiting...\n", mlen);
		exit(1);
	}
	new_statement->tag_size = tlen;
	new_statement->message_size = mlen;
	new_statement->log = malloc(tlen+mlen+1);
	strcpy(new_statement->log, tag);
	strcat(new_statement->log, message);
	lnm_registry_update();
	lnm_pushable_push(lnm_registered_items, (lnmItem)new_statement);
	return (lnmItem)new_statement;
}


lnmItem lnmEvent(void) {
	lnm_log_event * new_event = malloc(sizeof(lnm_log_event));
	new_event->type = 1;
	new_event->pushed = lnm_new_pushable();
	lnm_registry_update();
	lnm_pushable_push(lnm_registered_items, (lnmItem)new_event);
	return (lnmItem)new_event;
}

void lnmEventPush(lnmItem event, lnmItem item) {
	if (event == item) {
		printf("lognestmonster (lnmEventPush): attempt to push event to self. exiting...\n");
		exit(1);
	}
	lnm_log_statement * item_cast = (lnm_log_statement *)item;
	if (item_cast->boolpushed == 1) {
		printf("lognestmonster (lnmEventPush): attempt to push an already-pushed log item. exiting...\n");
		exit(1);
	}
	lnm_log_event * event_t = (lnm_log_event *)event;
	if (event_t->type != 1) {
		printf("lognestmonster (lnmEventPush): cannot cast non-event to event type. exiting...\n");
		exit(1);
	}
	lnm_pushable_push(event_t->pushed, item);
	item_cast->boolpushed = 1;
	lnm_registry_update();
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

void lnm_debug_parse_item(lnmItem item, int tabcount) {
	if (lnm_isstatement(item)) {
		lnm_log_statement * statement = (lnm_log_statement *) item;
		lnm_debug_tabs(tabcount);

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

		char tag[statement->tag_size+1];
		strncpy(tag, statement->log, statement->tag_size);
		tag[statement->tag_size] = '\0';

		char message[statement->message_size+1];
		strncpy(message, statement->log+statement->tag_size, statement->message_size);
		message[statement->message_size] = '\0';

		printf("%" PRIu64 " (%s) %s :: %s\n", statement->timestamp, verbosity, tag, message);
	} else if (!lnm_isstatement(item)) {
		lnm_log_event * event = (lnm_log_event *) item;
		lnm_debug_tabs(tabcount);
		printf("Event (%" PRIu32 ") [%" PRIu32 "] [\n", event->pushed->length, event->pushed->capacity);
		for (uint32_t i = 0; i < event->pushed->length; i++) {
			lnmItem item = event->pushed->pushed[i];
			lnm_debug_parse_item(item, tabcount + 1);
		}
		lnm_debug_tabs(tabcount);
		printf("]\n");
	} else {
		printf("lognestmonster (lnm_debug_parse_item): unknown item type. exiting...\n");
		exit(1);
	}
}

void lnm_debug_parse_registry(void) {
	printf("Top level registry (%" PRIu32 ") [%" PRIu32 "] [\n", lnm_registered_items->length, lnm_registered_items->capacity);
	for (uint32_t iter = 0; iter < lnm_registered_items->length; iter++) {
		lnm_debug_parse_item(lnm_registered_items->pushed[iter], 1);
	}
	printf("]\n");
}

void lnm_debug_parse_queue(lnmQueue queue) {
	lnm_queue * queue_cast = (lnm_queue *)queue;
	printf("Queue \"%s\" at %s (%" PRIu32 ") [%" PRIu32 "] [\n", queue_cast->name, queue_cast->out_path, queue_cast->pushed->length, queue_cast->pushed->capacity);
	for (uint32_t iter = 0; iter < queue_cast->pushed->length; iter++) {
		lnm_debug_parse_item((lnmItem)queue_cast->pushed->pushed[iter], 1);
	}
	printf("]\n");
}
#endif // DEFINE_LOGNESTMONSTER

#ifdef __cplusplus // Linker protection
}
#endif
