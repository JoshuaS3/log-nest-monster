<img src="/static/logo.png" height="200px"/>

_Multilevel logging for advanced programs._

1. [lognestmonster](#lognestmonster)
2. [Library Class Structure](#library-class-structure)
    1. [Semantics](#semantics)
3. [Serialization Format](#serialization-format)
    1. [Events](#events)
    2. [Statements](#statements)
        1. [Verbosity Level Enumeration](#verbosity-level-enumeration)
    3. [Example](#example)
4. [Temporary Data Saving](#temporary-data-saving)
5. [Copyright](#copyright)

# lognestmonster

## Library Class Structure
This is subject to future change over security concerns regarding pointers and memory allocation.
```
class lognestmonster

    enum VerbosityLevels {INFO, DEBUG, VERBOSE, VERYVERBOSE, WARNING, ERROR}

    struct QueueConfig
        char * out_dir // directory to output log files

    virtual void * alloc(size_t size)         // implementation defaults to cstd malloc()
    virtual void free(void * block)           // implementation defaults to cstd free()
    virtual void * serialize(LogObject * obj) // implementation defaults to manual serialization of standard LogObject to allocated block
    virtual bool write(void * serialized, size_t size, std::ostream stream, bool append) // implementation defaults to writing entire serialized block to stream
    virtual int delete(char * file_name)      // implementation defaults to cstd remove()

    interface LogObject
        Pushable * parent
        char * temp_file
        virtual bool save_temp()
        virtual bool delete_temp()

    interface Pushable
    protected:
        std::vector<LogObject *> pushed
    public:
        push(LogObject * obj)
        push(int verbosity, char * tag, char * message) // implicitly creates a Statement and then pushes

    class Queue : Pushable
    public:
        struct QueueConfig * _config
        constructor (struct QueueConfig * config)
        write()                                          // serializes, writes, and clears pushed LogObjects
        write(LogObject * obj)                           // implicit push(), then write()
        write(int verbosity, char * tag, char * message) // implicit Statement creation, push(), then write()

    class Event : LogObject, Pushable
    public:
        constructor (LogObject * obj)                           // implicit push()
        constructor (int verbosity, char * tag, char * message) // implicit Statement creation, then push()

    class Statement : LogObject
    public:
        int verbosity
        int timestamp
        std::string * tag
        std::string * message
        constructor (int verbosity, char * tag, char * message)
```
### Semantics
A `Queue` handles data serialization and file writing to the main logtree file. Queue writing refers to sending serialized logtree data to the outstream. Queue pushing refers to adding an Event or Statement to the queue for future writing.

An `Event` is a pushable list of statements or events, or the "nest". Event pushing refers to adding an Event or Statement to the parent's list.

A `Statement` is the data-containing log item with a timestamp, verbosity level, tag/invoker, and message.

In reference to data serialization, `parser` as used here is just a deserializer.

## Serialization Format

By default the library serializes log tree information in a special format. This can be overriden by anybody that uses the library.

### Metadata

All saved files should begin with an `unsigned char` version number and an `unsigned long long` millisecond timestamp.
```
unsigned char version
unsigned long long timestamp
```

### Events
Open event with `0x2` and close with `0x3`. Statements or more events can be written inbetween these tags.
```
0x2 // open event
    // more events or statements
0x3 // close event
```

### Statements
Open statement with `0x0` and close `0x1`.

1. 1 byte for an open statement tag
2. 1 byte for a predefined verbosity level enum
3. 4 bytes for an unsigned integer timestamp
4. 1 byte for the length of the tag string
5. 0-255 bytes for the tag string
6. 2 bytes for the length of the message string
7. 0-65535 bytes for the message string
8. 1 byte for a close statement tag

```
0x0
    unsigned char verbosity
    unsigned long long timestamp
    unsigned char tag_size
    unsigned char[] tag
    unsigned short message_size
    unsigned char[] message
0x1
```
A close statement tag is always needed in case the serializer method is overriden and provides extra data/metadata. If a close statement tag isn't written, a parser/deserializer won't be able to read a serialized logtree with extra data.

#### Verbosity Level Enumeration
The 6 verbosity level enums and their byte values are:
```
INFO        = 0
DEBUG       = 1
VERBOSE     = 2
VERYVERBOSE = 3
WARNING     = 4
ERROR       = 5
```

### Example
1 statement inside one 1 event:
```
1565561768719 // timestamp    8*
0x2     // open event         1
0x0     // open statement     1
1565561768752 // timestamp    8*
0       // verbosity          1
4       // tag_size           1
"INIT"  // tag                4*
5       // message_size       2
"HELLO" // message            5*
0x1     // close statement    1
0x3     // close event        1
        //                    33 total bytes for this log tree
```
With the sample log tree used here, the raw byte file totals 25 bytes. In use, a parser/deserializer could take this file and create output similar to the following:
```
lognestmonster - log_folder/
Size: 33 bytes | Timestamp: 1565561768719
1 Statement | 1 Event | 0 Unsaved Data Trees
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

v 1 ITEM
  1565561768752 - INFO - INIT - HELLO



::::::::::: press q to exit | arrow keys to move, expand, collapse :::::::::::
```

## Temporary Data Saving

By the nature of a push-write logging library, there's a chance that some created Statements and Events might not be pushed and written before the program's exit, whether it hangs, crashes, throws a runtime exception, is SIGKILLed, or anything else. Seeing as the point of logging is to find and diagnose errors with ease, it'd be frustrating to lose critical last-second information like this. The solution: save temporary serialized data for every creation or change to Statements or Events. Every logtree that ends in a Statement will have its own temporary data file; when a Statement is pushed to an Event, the Statement's file will be deleted and replaced into the greater Event file. See the following example for how data is separated into files:

```
Queue queue;
Event event;
Statement state1;
Statement state2;

// Existing files:
// statement1.raw
// statement2.raw

event.push(state1)

// Existing files:
// event.raw
// statement2.raw

queue.push(event)

// Existing files:
// event.raw
// statement2.raw

event.push(state2)

// Existing files:
// event.raw (all log items now exist inside the event, in the queue)

queue.write()

// Existing files:
// log12345.raw (consists of 2 statements inside 1 event)
```

In reality, file names will likely contain timestamps, hashes, UUIDs, or some other form of identifiable metadata.

## Copyright

lognestmonster Copyright (c) 2019 Joshua 'joshuas3' Stockin under the [GNU General Public License v3](LICENSE).

The following should be present in each file.
```
lognestmonster Copyright (c) 2019 Joshua 'joshuas3' Stockin
<https://github.com/JoshuaS3/lognestmonster/>.


This file is part of lognestmonster.

lognestmonster is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

lognestmonster is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with lognestmonster. If not, see <https://www.gnu.org/licenses/>.
```
