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


// Base definitions

enum lnmVerbosityLevel {lnmInfo, lnmDebug, lnmVerbose, lnmVeryVerbose, lnmWarning, lnmError};


// Pushable structure

typedef uint8_t * lnmItem;

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
	pushable->pushed = realloc(pushable->pushed, sizeof(lnmItem)*(pushable->length+1)); // reallocate with size: length+1
	pushable->pushed[pushable->length] = item;
	pushable->length += 1;
}


// Statement and event structure definitions

typedef struct {
	uint8_t          type; // Used internally; 0 = statement, 1 = event
	lnm_pushable * pushed; // array of memory locations for lnm_event and lnm_log_statement structs
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


// Core library

lnmItem lnmStatement(uint8_t verbosity, char * tag, char * message) {
	lnm_log_statement * new_statement = malloc(sizeof(lnm_log_statement));
	new_statement->type = 0;
	new_statement->verbosity = verbosity;
	new_statement->timestamp = 0;
	int tlen = strlen(tag);
	if (tlen > 255 || tlen < 0) {
		printf("lognestmonster: tag length %i is longer than the cap 255 characters. exiting...\n", tlen);
		exit(1);
	}
	int mlen = strlen(message);
	if (mlen > 65535 || mlen < 0) {
		printf("lognestmonster: message length %i is longer than the cap 65535 characters. exiting...\n", mlen);
		exit(1);
	}
	new_statement->tag_size = tlen;
	new_statement->message_size = mlen;
	new_statement->log = malloc(tlen+mlen+1);
	strcpy(new_statement->log, tag);
	strcat(new_statement->log, message);
	return (lnmItem)new_statement;
}

lnmItem lnmEvent() {
	lnm_log_event * new_event = malloc(sizeof(lnm_log_event));
	new_event->type = 1;
	new_event->pushed = lnm_new_pushable();
	return (lnmItem)new_event;
}

void lnmEventPush(lnmItem event, lnmItem item) {
	if (event == item) {
		printf("lognestmonster: attempt to push event to self. exiting...\n");
		exit(1);
	}
	lnm_pushable_push(((lnm_log_event*)event)->pushed, item);
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
	lnm_log_statement * statement = (lnm_log_statement *) item;
	if (statement->type == 0) {
		lnm_debug_tabs(tabcount);
		printf("Statement {\n");
		lnm_debug_tabs(tabcount+1);
		printf("Verbosity %i\n", statement->verbosity);
		lnm_debug_tabs(tabcount+1);
		printf("Timestamp %ld\n", statement->timestamp);
		lnm_debug_tabs(tabcount+1);
		printf("Log %s\n", statement->log);
		lnm_debug_tabs(tabcount);
		printf("}\n");
	} else if (statement->type == 1) {
		lnm_debug_tabs(tabcount);
		printf("Event {\n");
		lnm_log_event * event = (lnm_log_event *) item;
		for (int i = 0; i < event->pushed->length; i++) {
			lnmItem item = event->pushed->pushed[i];
			lnm_debug_parse(item, tabcount + 1);
		}
		lnm_debug_tabs(tabcount);
		printf("}\n");
	} else {
		printf("Bad item type\n");
		exit(1);
	}
}

#endif
