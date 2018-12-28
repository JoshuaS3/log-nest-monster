const Logger = require("../index.js");

Logger.Overseer = new Logger.Logger({
	name: "MyLogger",
	locations: {
		"node": "logs/test"
	}
});

let NodeQueue = Logger.Overseer.queue("node");
NodeQueue.push(Logger.INFO, "PROCESS", "Process started");
NodeQueue.push(Logger.INFO, "INIT", "Note that Statements can be directly written to the queue as Events can.");

let LoadEvent = new Logger.Event();
LoadEvent.push(Logger.INFO, "INIT", "We are now one level deep.");
LoadEvent.push(Logger.DEBUG, "NEW_TAG", "Keep note that you can still change verbosity level and tag/invoker with statements.");

let LowerNestedEvent = new Logger.Event();
LoadEvent.push(LowerNestedEvent);

LowerNestedEvent.push(Logger.INFO, "INIT", "I am a statement in LowerNestedEvent.");
LowerNestedEvent.push(Logger.DEBUG, "INIT", "We are now 2 layers deep.");

LoadEvent.push(Logger.DEBUG, "YEET", "Back to 1 layer deep.");
LoadEvent.push(Logger.INFO, "INIT", "Finished.");

NodeQueue.push(LoadEvent);

NodeQueue.push(Logger.INFO, "INIT", "LoadEvent has now been pushed to the queue. Time to write the queue.");

NodeQueue.write();
