const Logger = {
	Logger: require("./src/logger.js"),
	Event: require("./src/event.js"),
	Statement: require("./src/statement.js"),
	Queue: require("./src/queue.js")
}


var MyLogger = new Logger.Logger({
	name: "MyLogger", // This serves no use in the creation of log files, it's just identification for the program
	locations: { // The names of locations and their corresponding log directories
		"node": "./log/node",
		"http": "./log/http"
	},
});

let NodeLogQueue = MyLogger.queue("node"); // selects the "node" location log queue

let LoadEvent = new Logger.Event(); // creates a new Event, a nest for Statements

// Statement objects contain [timestamp, verbosity, tag, message] variables and are the containers for all data

// Queue.push(statement);
// Queue.push(verbosity, tag, message); - implicitly creates a Statement object
// Queue.push(event); - in this case, the Queue object pushes the `event.statements` table
NodeLogQueue.push(LoadEvent); // This places LoadEvent at the front of the to-write-to-node-log queue.
// Note in most scenarios you would want to empty the queue as soon as it's populated, so waiting until
// the event is written before emptying isn't wise. In this case, because NodeLogQueue has an event
// pushed to it before the event is finished, the event could be prematurely processed by another
// synchronous `.write()` call to the queue object. This demonstration is only okay because there is
// only one `.write()` call to the queue object, which is after the Event object is written.


// Although not used here, the Statement object is created with the same parameters used below (verbosity, tag, message)
// Event.push(verbosity, tag, message); - implicitly creates a Statement object
// Event.push(event); - in this case, the Event object pushes the `event.statements` table

LoadEvent.push("INFO", "INIT", "Acquiring needed top-level packages.");


let LowerNestedEvent = new Logger.Event();

LowerNestedEvent.push("INFO", "INIT", "Loading fs...");
LowerNestedEvent.push("DEBUG", "INIT", "fs loaded."); // Verbosity levels and tags are still available for result filtering

LowerNestedEvent.push("INFO", "INIT", "Loading http...");
LowerNestedEvent.push("DEBUG", "INIT", "http loaded.");

LowerNestedEvent.push("INFO", "INIT", "Loading jsonwebtoken...");
LowerNestedEvent.push("DEBUG", "INIT", "jsonwebtoken loaded.");

LowerNestedEvent.push("INFO", "INIT", "Loading lognestmonster...");
LowerNestedEvent.push("DEBUG", "INIT", "lognestmonster loaded.");



LoadEvent.push(LowerNestedEvent);
LoadEvent.push("INFO", "INIT", "Finished.");

NodeLogQueue.write(); // Makes the queue append all to file and empty itself

/*

A possible parsing system may look like this:

-------------------------------------------------------------------------------------


[[NAME]]
[[TIMESTAMP]]
[[LOG FILESIZE]]
[[LOG ITEM COUNT]]
> 3 ITEMS


-------------------------------------------------------------------------------------


[[NAME]]
[[TIMESTAMP]]
[[LOG FILESIZE]]
[[LOG ITEM COUNT]]
v 3 ITEMS
	TIMESTAMP - INFO - INIT - Acquiring needed top-level packages.
	> 4 ITEMS
	TIMESTAMP - INFO - INIT - Finished.


-------------------------------------------------------------------------------------


[[NAME]]
[[TIMESTAMP]]
[[LOG FILESIZE]]
[[LOG ITEM COUNT]]
v 3 ITEMS
	TIMESTAMP - INFO - INIT - Acquiring needed top-level packages.
	v 4 ITEMS
		TIMESTAMP - INFO - INIT - Loading fs...
		TIMESTAMP - INFO - INIT - Loading http...
		TIMESTAMP - INFO - INIT - Loading jsonwebtoken...
		TIMESTAMP - INFO - INIT - Loading lognestmonster...
	TIMESTAMP - INFO - INIT - Finished.


*/


console.log(JSON.stringify(LoadEvent.statements));

