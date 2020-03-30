/* lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin
 * <https://joshstock.in>
 * <https://github.com/JoshuaS3/lognestmonster>
 *
 * This software is licensed and distributed under the terms of the MIT License:
 * ----- BEGIN LICENSE -----
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 * ----- END LICENSE -----
 *
 * This comment block and its contents, including this disclaimer, MUST be
 * preserved in all copies or distributions of this software's source.
 */

// lognestmonster.h
// C header file for implementation of the lognestmonster logging library


#ifndef LOGNESTMONSTER_H
#define LOGNESTMONSTER_H 1


#ifdef __cplusplus
extern "C" {
#endif


#include <stdint.h>  // necessary include for type declaration


enum lnmVerbosityLevel {lnmInfo, lnmDebug, lnmVerbose, lnmVeryVerbose, lnmWarning, lnmError};
typedef uint8_t * lnmItem;
typedef uint8_t * lnmQueue;


lnmQueue lnmQueueInit(const char * name, const char * out_path);
lnmQueue lnmQueueByName(const char * name);

lnmItem lnmStatement(enum lnmVerbosityLevel verbosity, const char * message);

lnmItem lnmEvent(const char * tag);
lnmItem lnmEventI(const char * tag, lnmItem item);
lnmItem lnmEventS(const char * tag, enum lnmVerbosityLevel verbosity, const char * message);
void lnmEventPush(lnmItem event, lnmItem item);
void lnmEventPushS(lnmItem event, enum lnmVerbosityLevel verbosity, const char * message);


#ifdef LNM_ALL  // expose private utilities

// type definitions
typedef struct lnm_pushable lnm_pushable;
typedef struct lnm_log_event lnm_log_event;
typedef struct lnm_log_statement lnm_log_statement;
typedef struct lnm_queue lnm_queue;

// lnm_pushable utilities
lnm_pushable * lnm_new_pushable(void);
void lnm_pushable_realloc(lnm_pushable * pushable);
void lnm_pushable_push(lnm_pushable * pushable, lnmItem item);
void lnm_pushable_pop(lnm_pushable * pushable);
void lnm_pushable_remove(lnm_pushable * pushable, uint32_t index);
void lnm_pushable_free(lnm_pushable * pushable);

// misc utilities
_Noreturn void lnm_abort(const char * function_traceback, const char * message);
unsigned long lnm_getus(void);

// registry utilities
void lnm_registry_update(void);

// memory management utilities
void lnm_free_item(lnmItem item);
void lnm_free_registry(void);
void lnm_free_queue(lnmQueue queue);

#endif  // LNM_ALL


#if defined(LNM_DEBUG) || defined(LNM_ALL)
void lnm_debug_tabs(int tab_count);
void lnm_debug_parse_item(lnmItem item, int tab_count);
void lnm_debug_parse_registry(void);
void lnm_debug_parse_queue(lnmQueue queue);
#endif  // LNM_DEBUG || LNM_ALL


#ifdef LNM_INIT  // define the library


#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


enum LNM_ITEM_TYPE {
	LNM_STATEMENT = 0,
	LNM_EVENT = 1,
};


_Noreturn void lnm_abort(const char * function_traceback, const char * message) {
	printf("lognestmonster (%s): %s. aborting...\n", function_traceback, message);
	abort();
}


// lnm_pushable utilities


typedef struct lnm_pushable {
	uint32_t capacity;
	uint32_t length;
	lnmItem * frame;
} lnm_pushable;


void lnm_pushable_realloc(lnm_pushable * pushable) {
	if (pushable->length > pushable->capacity) {
		if (pushable->capacity > UINT32_MAX / 2) {
			lnm_abort("lnm_pushable_realloc", "pushable can't surpass max capacity of 2^16");
		}
		pushable->frame = realloc(pushable->frame, sizeof(lnmItem) * (pushable->capacity *= 2));
		if (pushable->frame == NULL) {
			lnm_abort("lnm_pushable_realloc", "call to realloc() returned NULL");
		}
	} else if (pushable->length < (pushable->capacity / 2)) {
		while (pushable->length < (pushable->capacity / 2) && pushable->capacity > 8) {
			pushable->capacity /= 2;
		}
		pushable->frame = realloc(pushable->frame, sizeof(lnmItem) * (pushable->capacity));
		if (pushable->frame == NULL) {
			lnm_abort("lnm_pushable_realloc", "call to realloc() returned NULL");
		}
	}
}


lnm_pushable * lnm_new_pushable(void) {
	lnm_pushable * new_pushable = calloc(1, sizeof(lnm_pushable));
	if (new_pushable == NULL) {
		lnm_abort("lnm_new_pushable", "call to calloc() returned NULL");
	}
	new_pushable->capacity = 8;
	new_pushable->length = 0;
	new_pushable->frame = calloc(8, sizeof(lnmItem));
	if (new_pushable->frame == NULL) {
		lnm_abort("lnm_new_pushable", "call to calloc() returned NULL");
	}
	return new_pushable;
}


void lnm_pushable_push(lnm_pushable * pushable, lnmItem item) {
	pushable->length++;
	lnm_pushable_realloc(pushable);
	pushable->frame[pushable->length - 1] = item;
}


void lnm_pushable_pop(lnm_pushable * pushable) {
	pushable->length--;
	lnm_pushable_realloc(pushable);
}


void lnm_pushable_remove(lnm_pushable * pushable, uint32_t index) {
	if (index >= pushable->length) {
		lnm_abort("lnm_pushable_remove", "attempt to remove index out of pushable bounds");
	}
	if (index == pushable->length - 1) {
		lnm_pushable_pop(pushable);
	} else {
		// shift entire array from index until end
		for (uint32_t iter = index; iter < pushable->length - 1; iter++) {
			pushable->frame[iter] = pushable->frame[iter + 1];
		}
		pushable->length--;
		lnm_pushable_realloc(pushable);
	}
}


void lnm_pushable_free(lnm_pushable * pushable) {
	free(pushable->frame);
	free(pushable);
}


// log event and log statement definitions


typedef struct lnm_log_event {
	// word 1, 1 byte data 7 bytes padding
	uint8_t        type:1;      // used internally; 0 = statement, 1 = event
	uint8_t        pushed:1;    // whether or not this log item has been pushed

	// word 2, 8 bytes data
	char *         tag;         // null-terminated tag string

	// word 3, 8 bytes data
	lnm_pushable * pushable;    // pushable of lnmItems
} lnm_log_event;


typedef struct lnm_log_statement {
	// word 1, 1 byte data 7 bytes padding
	uint8_t  type:1;       // used internally; 0 = statement, 1 = event
	uint8_t  pushed:1;     // whether or not this log item has been pushed
	uint8_t  verbosity:3;  // lnmVerbosityLevel, 0-5

	// word 2, 8 bytes data
	uint64_t timestamp;    // 64-bit millisecond timestamp

	// word 3, 8 bytes data
	char *   log;          // null-terminated message string
} lnm_log_statement;


// queue structure definition


typedef struct lnm_queue {
	char * name;
	char * out_path;
	uint64_t timestamp;
	lnm_pushable * pushable;
} lnm_queue;


// time utilities


#if defined(__unix__) || defined(unix) || defined(__unix) || defined(__CYGWIN__)
#include <sys/time.h>
uint64_t lnm_getus(void) {
	uint64_t us;
	struct timeval lnm_current_time;
	gettimeofday(&lnm_current_time, NULL);
	us = (lnm_current_time.tv_sec*1000000+lnm_current_time.tv_usec);
	return us;
}
#elif defined(_WIN32) || defined(__WINDOWS__)
#include <windows.h>
#include <sysinfoapi.h>
uint64_t lnm_getus(void) {
	uint64_t us;
	// get system time in ticks
	FILETIME lnm_win32_filetime;
	GetSystemTimeAsFileTime(&lnm_win32_filetime);
	// load time from two 32-bit words into one 64-bit integer
	us = lnm_win32_filetime.dwHighDateTime;
	us = us << 32;
	us |= lnm_win32_filetime.dwLowDateTime;
	// convert to microseconds
	us /= 10;
	// convert from time since Windows NT epoch to time since Unix epoch
	us -= 11644473600000000ULL;
	return us;
}
#else
#error lognestmonster: Neither Windows NT nor a POSIX-compliant system were detected.\
		Implement your own system time functions or compile on a compliant system.
#endif


// item registry utils


void lnm_free_item(lnmItem item);
static lnm_pushable * lnm_registered_queues;
static lnm_pushable * lnm_registered_items;


void lnm_registry_update(void) {
	// iterate through registry
	for (uint32_t iter = 0; iter < lnm_registered_items->length; iter++) {
		lnm_log_statement * item = (lnm_log_statement *)(lnm_registered_items->frame[iter]);
		// if the registered item has been pushed elsewhere, remove it from the top level of the registry
		if (item->pushed) {
			lnm_pushable_remove(lnm_registered_items, iter);
			iter--;
		}
	}
}


void lnm_registry_push(lnmItem item) {
	if (lnm_registered_items == NULL) {
		lnm_registered_items = lnm_new_pushable();
	}
	lnm_pushable_push(lnm_registered_items, item);
}


void lnm_registry_free() {
	lnm_registry_update();
	for (uint32_t iter = 0; iter < lnm_registered_items->length;) {
		lnm_free_item(lnm_registered_items->frame[lnm_registered_items->length-1]);
	}
	lnm_pushable_realloc(lnm_registered_items);
}


void lnm_registry_flush_item(lnmItem item) {
	lnm_log_statement * item_cast = (lnm_log_statement *)item;
	if (!item_cast->pushed) {
		item_cast->pushed = 1;
		lnm_registry_update();
	}
}


// core library utilities


int lnm_item_type(lnmItem item) {
	return ((lnm_log_statement *)item)->type;
}

void lnm_free_item(lnmItem item) {
	if (lnm_item_type(item) == LNM_STATEMENT) {
		// cast item
		lnm_log_statement * statement = (lnm_log_statement *)item;
		// flush item out of registry
		lnm_registry_flush_item(item);
		// free item and its contents
		free(statement->log);
		free(statement);
	} else if (lnm_item_type(item) == LNM_EVENT) {
		// create breadcrumb navigation array with root 'item'
		lnm_pushable * breadcrumb = lnm_new_pushable();
		lnm_pushable_push(breadcrumb, item);
		// continually iterate breadcrumb until it's empty
		while (breadcrumb->length > 0) {
			// get current item (deepest element of the breadcrumb nav, aka 'z' in 'x > y > z')
			lnmItem current = breadcrumb->frame[breadcrumb->length - 1];
			// pop it from the breadcrumb nav
			lnm_pushable_pop(breadcrumb);
			// flush item out of registry
			lnm_registry_flush_item(current);
			if (lnm_item_type(current) == LNM_STATEMENT) {
				// cast current item
				lnm_log_statement * current_statement = (lnm_log_statement *)current;
				// free statement and its contents
				free(current_statement->log);
				free(current_statement);
				continue;
			} else if (lnm_item_type(current) == LNM_EVENT) {
				// cast current item
				lnm_log_event * current_event = (lnm_log_event *)current;
				if (current_event->pushable->length > 0) {
					// the event has children, add them to the breadcrumb
					for (uint32_t iter = 0; iter < current_event->pushable->length; iter++) {
						lnmItem current_event_child = current_event->pushable->frame[iter];
						lnm_pushable_push(breadcrumb, current_event_child);
					}
				}
				// free original event
				lnm_pushable_free(current_event->pushable);
				free(current_event->tag);
				free(current_event);
				continue;
			} else {
				lnm_abort("lnm_free_item", "item in log tree has non-statement and non-event type");
			}
		}
		lnm_pushable_free(breadcrumb);
	} else {
		lnm_abort("lnm_free_item", "log tree is non-statement and non-event type");
	}
}


// queue utilities


void lnm_free_queue(lnmQueue queue) {
	lnm_queue * queue_cast = (lnm_queue *)queue;
	for (uint32_t iter = 0; iter < queue_cast->pushable->length; iter++) {
		lnm_free_item(queue_cast->pushable->frame[iter]);
		lnm_pushable_remove(queue_cast->pushable, iter);
		iter--;
	}
}


lnmQueue lnmQueueInit(const char * name, const char * out_path) {
	// create queue and item registries if not created
	if (lnm_registered_queues == NULL) {
		lnm_registered_queues = lnm_new_pushable();
	}
	if (lnm_registered_items == NULL) {
		lnm_registered_items = lnm_new_pushable();
	}
	// allocate and populate a new Queue object
	lnm_queue * new_queue = calloc(1, sizeof(lnm_queue));
	if (new_queue == NULL) {
		lnm_abort("lnmQueueInit", "call to calloc() returned NULL");
	}
	new_queue->name = malloc(strlen(name)+1);
	new_queue->out_path = malloc(strlen(out_path)+1);
	if (new_queue->name == NULL || new_queue->out_path == NULL) {
		lnm_abort("lnmQueueInit", "call to malloc() returned NULL");
	}
	strcpy(new_queue->name, name);
	strcpy(new_queue->out_path, out_path);
	new_queue->timestamp = lnm_getus();
	new_queue->pushable = lnm_new_pushable();
	// enter new Queue into registry
	lnm_pushable_push(lnm_registered_queues, (lnmQueue)new_queue);
	return (lnmQueue)new_queue;
}


lnmQueue lnmQueueByName(const char * name) {
	if (lnm_registered_queues == NULL) {
		lnm_abort("lnmQueueByName", "queue registry is nonexistent");
	}
	if (lnm_registered_queues->length == 0) {
		lnm_abort("lnmQueueByName", "queue registry is empty");
	}
	for (uint32_t iter = 0; iter < lnm_registered_queues->length; iter++) {
		lnm_queue * queue = (lnm_queue *)lnm_registered_queues->frame[iter];
		if (strcmp(queue->name, name) == 0) {
			return (lnmQueue)queue;
		}
	}
	lnm_abort("lnmQueueByName", "queue not found in registry");
}


void lnmQueuePush(lnmQueue queue, lnmItem item) {
	if (queue == NULL || item == NULL) {
		lnm_abort("lnmQueuePush", "cannot perform operation on NULL arguments");
	}
	lnm_log_statement * statement = (lnm_log_statement *)item;
	if (statement->pushed == 1) {
		lnm_abort("lnmQueuePush", "attempt to push an already-pushed log item");
	}
	// flush out of registry
	lnm_registry_flush_item(item);
	// add to queue
	lnm_pushable_push(((lnm_queue *)queue)->pushable, item);
}


lnmItem lnmStatement(enum lnmVerbosityLevel verbosity, const char * message) {
	if (message == NULL) {
		lnm_abort("lnmStatement", "cannot perform operation on NULL argument");
	}
	lnm_log_statement * new_statement = calloc(1, sizeof(lnm_log_statement));
	if (new_statement == NULL) {
		lnm_abort("lnmStatement", "call to calloc() returned NULL");
	}
	new_statement->type = LNM_STATEMENT;
	new_statement->pushed = 0;
	new_statement->verbosity = verbosity;
	new_statement->timestamp = lnm_getus();
	// enforce string lengths
	int message_len = strlen(message) + 1;
	// copy message to new_statement->log
	new_statement->log = malloc(message_len);
	if (new_statement->log == NULL) {
		lnm_abort("lnmStatement", "call to malloc() returned NULL");
	}
	strcpy(new_statement->log, message);
	// add to registry
	lnm_registry_push((lnmItem)new_statement);
	return (lnmItem)new_statement;
}


lnmItem lnmEvent(const char * tag) {
	if (tag == NULL) {
		lnm_abort("lnmEvent", "cannot perform operation on NULL argument");
	}
	lnm_log_event * new_event = calloc(1, sizeof(lnm_log_event));
	if (new_event == NULL) {
		lnm_abort("lnmEvent", "call to calloc() returned NULL");
	}
	new_event->type = LNM_EVENT;
	new_event->pushed = 0;
	new_event->pushable = lnm_new_pushable();
	// copy tag to event
	int tag_len = strlen(tag) + 1;
	new_event->tag = malloc(tag_len);
	if (new_event->tag == NULL) {
		lnm_abort("lnmEvent", "call to malloc() returned NULL");
	}
	strcpy(new_event->tag, tag);
	// add to registry
	lnm_registry_push((lnmItem)new_event);
	return (lnmItem)new_event;
}


void lnmEventPush(lnmItem event, lnmItem item) {
	if (event == NULL || item == NULL) {
		lnm_abort("lnmEventPush", "cannot perform operation on NULL arguments");
	}
	if (event == item) {
		lnm_abort("lnmEventPush", "attempt to push event to self");
	}
	lnm_log_statement * item_cast = (lnm_log_statement *)item;
	if (item_cast->pushed == 1) {
		lnm_abort("lnmEventPush", "attempt to push an already-pushed log item");
	}
	if (lnm_item_type(event) != LNM_EVENT) {
		lnm_abort("lnmEventPush", "cannot cast non-event to event type");
	}
	lnm_log_event * event_cast = (lnm_log_event *)event;
	lnm_pushable_push(event_cast->pushable, item);
	lnm_registry_flush_item(item);
}


void lnmEventPushS(lnmItem event, enum lnmVerbosityLevel verbosity, const char * message) {
	lnmItem statement = lnmStatement(verbosity, message);
	lnmEventPush(event, statement);
}


lnmItem lnmEventI(const char * tag, lnmItem item) {
	lnmItem event = lnmEvent(tag);
	lnmEventPush(event, item);
	return event;
}


lnmItem lnmEventS(const char * tag, enum lnmVerbosityLevel verbosity, const char * message) {
	lnmItem event = lnmEvent(tag);
	lnmEventPushS(event, verbosity, message);
	return event;
}


#ifdef LNM_DEBUG
#include <inttypes.h>

void lnm_debug_tabs(int tab_count) {
	for (int i = 0; i < tab_count; i++) {
		printf("  ");
	}
}


void lnm_debug_parse_item(lnmItem item, int tab_count) {
	if (lnm_item_type(item) == LNM_STATEMENT) {
		lnm_log_statement * statement = (lnm_log_statement *) item;
		lnm_debug_tabs(tab_count);

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

		printf("%" PRIu64 " (%s) :: %s\n", statement->timestamp, verbosity, statement->log);
	} else if (lnm_item_type(item) == LNM_EVENT) {
		lnm_log_event * event = (lnm_log_event *) item;
		lnm_debug_tabs(tab_count);
		printf("Event (%" PRIu32 "/%" PRIu32 ") %s [\n", event->pushable->length, event->pushable->capacity, event->tag);
		for (uint32_t iter = 0; iter < event->pushable->length; iter++) {
			lnmItem item = event->pushable->frame[iter];
			lnm_debug_parse_item(item, tab_count + 1);
		}
		lnm_debug_tabs(tab_count);
		printf("]\n");
	} else {
		lnm_abort("lnm_debug_parse_item", "unknown item type");
	}
}


void lnm_debug_parse_registry(void) {
	printf("Top level registry (%" PRIu32 "/%" PRIu32 ") [\n", lnm_registered_items->length, lnm_registered_items->capacity);
	for (uint32_t iter = 0; iter < lnm_registered_items->length; iter++) {
		lnm_debug_parse_item(lnm_registered_items->frame[iter], 1);
	}
	printf("]\n");
}


void lnm_debug_parse_queue(lnmQueue queue) {
	lnm_queue * queue_cast = (lnm_queue *)queue;
	printf("Queue \"%s\" at %s (%" PRIu32 "/%" PRIu32 ") [\n", queue_cast->name, queue_cast->out_path, queue_cast->pushable->length, queue_cast->pushable->capacity);
	for (uint32_t iter = 0; iter < queue_cast->pushable->length; iter++) {
		lnm_debug_parse_item((lnmItem)queue_cast->pushable->frame[iter], 1);
	}
	printf("]\n");
}
#endif  // LNM_DEBUG
#endif  // LNM_INIT


#ifdef __cplusplus
}
#endif


#endif  // LOGNESTMONSTER_H
