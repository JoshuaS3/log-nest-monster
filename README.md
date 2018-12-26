<img src="/static/logo.png" height="200px"/>

_Advanced node.js logging for advanced programs._

# log-nest-monster
Most loggers available only use a _linear_ method of logging; there are verbosity levels and tags to narrow searches, but everything is still on the same level or plane nonetheless. The package `lognestmonster` is a similar type of logger, but it allows you to create multiple **layers** (or "**nests**") of log statements. This is useful because, although you may have to put in some extra organizational work on the code side, the log results are much more clean and thorough, boosting workflow efficiency. The user has absolute control over the way log statements are pushed to their log files.

_Why should I use this?_ There are many projects that create insane amounts of data, almost impossible to sift through without a helper program. The purpose of this logging system is to be a time-saver. Although it takes more time to put it in place, it's almost immediately made up with the performance gain through using the new log format. One thing that's unique about this logger compared to others is that it allows multiple queues to be made, in turn allowing you to split up your data. For example, a Node web server could keep one log file that records everything that the backend does while it uses another to record user or traffic information for analytics. Parsing software could be used to read either one.

## Classes

There are 4 classes offered by the package: `Logger`, the driving device that organizes everything; `Queue`, the class that actually pushes the log statements to their respective file; `Statement`, the actual log data (timestamp, verbosity, tag/invoker, message); and `Event`, a nest layer for `Statement`s or other `Event`s.

The following subsections assume that `lognestmonster` has been `require`d by node.js with the following code:
```javascript
const Logger = require("lognestmonster");
```

### Logger

Creates and organizes your queues. `Logger` is the exported package. `Logger.Logger` is the Logger class.

Logger.Logger()
```javascript
var MyLogger = new Logger.Logger(Object config);
```
Where `Object config` defaults to:
```json
{"name": "Logger", "locations": {"node": "./log/node"}}
```
`name` serves no purpose other than identification. `locations` is used to create new queues, taking each key as the queue name and each value as the queue output location.

Logger.Logger.queue()
```javascript
MyLogger.queue(string name);
```
This returns the appropriate `Queue` object for the provided `name`, assuming it was created with the `Logger` object.

### Queue

Manages log `Statement`s and `Event`s and how they're written to the final log file. Note that these are implicitly created with `Logger.Logger` when the `locations` object is properly provided in the `config` parameter of the `Logger.Logger` constructor.

Logger.Queue()
```javascript
let MyQueue = new Logger.Queue(string name, string location);
// note that parameters are the same format as key-value
// pairs in `config.locations` of `Logger.Logger(config)`
```
This creates the queue, taking `name` to be used as its ID and `location` as the path to where the log file should be created.

Logger.Queue.push()
```javascript
MyQueue.push(Statement statement);
MyQueue.push(Event event);
MyQueue.push(string verbosity, string tag, string message); // implicitly creates a `Statement` object
```
This adds log items or nests to the to-write queue. This returns the Queue object.

Logger.Queue.write()
```javascript
MyQueue.write();
```
This appends every queue value to the log file, emptying the queue. This returns the Queue object.

### Statement

This is the base log item where written log data is actually held.

Logger.Statement()
```javascript
let MyStatement = Logger.Statement(string verbosity, string tag, string message);
```

The timestamp value is created automatically by the constructor.

### Event

This is the proper name for a nest. Essentially, it's just an array that can hold other `Event` objects and `Statement` objects, creating a tree.

Logger.Event()
```javascript
let MyEvent = Logger.Event();
let MyEvent = Logger.Event(Event event);
let MyEvent = Logger.Event(Statement statement);
let MyEvent = Logger.Event(string verbosity, string tag, string message);
```
Any arguments given are passed to `this.push()`.

Logger.Event.push()
```javascript
MyEvent.push(Event event);
MyEvent.push(Statement statement);
MyEvent.push(string verbosity, string tag, string message);
```
This message pushes an `Event` or `Statement` as items in the nest. In the case that 3 strings are given as arguments, a `Statement` is implicitly created. This returns the Event object.

## Verbosity Levels

When creating a `Statement`, you can pass anything you'd like for the first `verbosity` string, although there are some ones preset by the package:

`Logger.INFO`
`Logger.DEBUG`
`Logger.VERBOSE`
`Logger.VERYVERBOSE`
`Logger.WARNING`
`Logger.ERROR`

These verbosity levels can be used to narrow down your search results when parsing the log files.

## Sample Usage

Here's an example of how somebody would initiate the Logger, create and push items to the Queue, and write them to the log file. **PLEASE SEE THE NOTES ABOUT THIS EXAMPLE DOWN BELOW.**
```javascript
// Require the package
const Logger = require("lognestmonster");

// Creates the logger object. Placing the new Logger inside the package allows cross-file usage, so you only have to initiate once.
Logger.Overseer = new Logger.Logger({
	name: "Overseer",
	locations: {
		"node": "./log/node" // Creates a queue named `node` that uses the path `./log/node`
	},
});

// Pushes a statement directly to the `node` queue
Logger.Overseer.queue("node").push(Logger.INFO, "PROCESS", "Process started");

// Creates a new event and pushes a Statement to it
let LoadEvent = new Logger.Event();
LoadEvent.push(Logger.INFO, "INIT", "Acquiring needed top-level packages.");

// Creates a new event and pushes multiple Statements to it
let LowerNestedEvent = new Logger.Event();

LowerNestedEvent.push(Logger.INFO, "INIT", "Loading fs...");
LowerNestedEvent.push(Logger.DEBUG, "INIT", "fs loaded.");

LowerNestedEvent.push(Logger.INFO, "INIT", "Loading http...");
LowerNestedEvent.push(Logger.DEBUG, "INIT", "http loaded.");

LowerNestedEvent.push(Logger.INFO, "INIT", "Loading jsonwebtoken...");
LowerNestedEvent.push(Logger.DEBUG, "INIT", "jsonwebtoken loaded.");

LowerNestedEvent.push(Logger.INFO, "INIT", "Loading lognestmonster...");
LowerNestedEvent.push(Logger.DEBUG, "INIT", "lognestmonster loaded.");

// Pushes the Event LowerNestedEvent to the Event LoadEvent
LoadEvent.push(LowerNestedEvent);

// Pushes another statement to LoadEvent
LoadEvent.push(Logger.INFO, "INIT", "Finished.");

// Pushes LoadEvent (a nest that consists of [Statement, Event, Statement] now) to the write queue
Logger.Overseer.queue("node").push(LoadEvent);

// Queue should now look like this: [Statement, Event]

// Writes the queue, effectively emptying it into the log file
Logger.Overseer.queue("node").write();
```

The above code creates the following JSON-like log output in the designated file:
```json
{"timestamp":"2018-12-26T18:08:37.654Z","verbosity":"INFO","tag":"PROCESS","message":"Process started"}
[{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Acquiring needed top-level packages."},[{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading fs..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"fs loaded."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading http..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"http loaded."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading jsonwebtoken..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"jsonwebtoken loaded."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading lognestmonster..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"lognestmonster loaded."}],{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Finished."}]
```

_To see how to parse this data (putting it into proper JSON), see the Log Format section._

### Notes about this example

_Large projects_
If your project spans multiple files, you could easily place your Logger object into the package itself, allowing the same Logger object to be accessed by other parts of your project. This is seen in the sample code with `Logger.Overseer = new Logger.Logger(...)`.

_Repetition_
There is some repetitive code; specifically, `Logger.Overseer.queue("node")`. Do note that this actually results in a `Queue` object, so you could easily make this its own variable like this:
```javascript
let NodeQueue = Logger.Overseer.queue("node");
NodeQueue.push(...).write();
```

_Queue pushing and writing_
When you're pushing multiple objects to a queue, be wary that they will stay there until the queue is written. Because everything is its own class, what you're really pushing is a _reference_ to the real object, so you can make changes to a pushed object after it has been pushed. As such, it is entirely possible to prematurely write a queue before an already-pushed `Event` or `Statement` is finished. It's good practice to immediately write the queue immediately after it has been pushed. Perhaps in the future there will be some functionality where a `Statement` or `Event` can be directly written instead of placed in the queue.

_Push order_
The developer has control over **everything** here. The order of your log file is the order that you push to your `Event`s and `Queue`. If I were to push a new Statement to `LoadEvent` in the middle of the pushes to `LowerNestedEvent`, it would show up on the log first because `LowerNestedEvent` isn't itself pushed to `LoadEvent` until later in the code. The order of the log file is 100% logical and in the developer's control, so it would be wise to write your code neatly with this in mind. This logging package doesn't do anything you don't tell it to.

## Log Format

Logs are controlled by `Queue` objects. Placed in the folder they're told, the logs should follow the ISO datetime format and have a `.log` file extension. Here's the name of a sample log file: `2018-12-26T18-08-37-653Z.log`

Regarding format, logs follow a JSON-like format, as follows:
```json
{"timestamp":"2018-12-26T18:08:37.654Z","verbosity":"INFO","tag":"PROCESS","message":"Process started"}
[{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Acquiring needed top-level packages."},[{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading fs..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"fs loaded."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading http..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"http loaded."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading jsonwebtoken..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"jsonwebtoken loaded."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Loading lognestmonster..."},{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"DEBUG","tag":"INIT","message":"lognestmonster loaded."}],{"timestamp":"2018-12-26T18:08:37.655Z","verbosity":"INFO","tag":"INIT","message":"Finished."}]
```

Because of the way the Queue objects push it (the most efficient way regarding computing power with changing/appending to files), you will have to do a bit of tweaking to get it in proper JSON format:

1. Add a comma before every newline (except for the last one at the end of the file)
2. Wrap everything in table brackets ('[' and ']')

This could be easily automated. Once finished, you get proper JSON (below), where each object `{}` is a Statement and each wrapping table `[]` is an Event (excluding the outermost one).

```json
[
  {
    "timestamp": "2018-12-26T05:55:23.360Z",
    "verbosity": "INFO",
    "tag": "PROCESS",
    "message": "Process started"
  },
  [
    {
      "timestamp": "2018-12-26T05:55:23.360Z",
      "verbosity": "INFO",
      "tag": "INIT",
      "message": "Acquiring needed top-level packages."
    },
    [
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "INFO",
        "tag": "INIT",
        "message": "Loading fs..."
      },
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "DEBUG",
        "tag": "INIT",
        "message": "fs loaded."
      },
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "INFO",
        "tag": "INIT",
        "message": "Loading http..."
      },
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "DEBUG",
        "tag": "INIT",
        "message": "http loaded."
      },
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "INFO",
        "tag": "INIT",
        "message": "Loading jsonwebtoken..."
      },
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "DEBUG",
        "tag": "INIT",
        "message": "jsonwebtoken loaded."
      },
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "INFO",
        "tag": "INIT",
        "message": "Loading lognestmonster..."
      },
      {
        "timestamp": "2018-12-26T05:55:23.360Z",
        "verbosity": "DEBUG",
        "tag": "INIT",
        "message": "lognestmonster loaded."
      }
    ],
    {
      "timestamp": "2018-12-26T05:55:23.360Z",
      "verbosity": "INFO",
      "tag": "INIT",
      "message": "Finished."
    }
  ]
]
```

The above can be taken in by parsing software and create something similar to the following:

```
[[LOG FILE NAME]]
[[LOG DATE]]
[[LOG FILE SIZE]]
[[LOG ITEM COUNT]]

TIMESTAMP - INFO - PROCESS - Process started
v 3 ITEMS
	TIMESTAMP - INFO - INIT - Acquiring needed top-level packages.
	v 6 ITEMS
		TIMESTAMP - INFO - INIT - Loading fs...
		TIMESTAMP - DEBUG - INIT - fs loaded.
		TIMESTAMP - INFO - INIT - Loading http...
		TIMESTAMP - DEBUG - INIT - http loaded.
		TIMESTAMP - INFO - INIT - Loading jsonwebtoken...
		TIMESTAMP - DEBUG - INIT - jsonwebtoken loaded.
	TIMESTAMP - INFO - INIT - Finished.
```

This is exciting! You still have the ability to narrow down your results with timestamps, verbosity levels, and tags/invokers, but now you have the organization with collapsable nests to not be overwhelmed with large amounts of data at the same time.

## Contributors

Developer - Joshua 'joshuas3' Stockin \<joshstockin@gmail.com\> (https://www.github.com/joshuas3)

Name - Patrik 'Patrola' Xop (https://github.com/PatrikXop)
