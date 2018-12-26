const Logger = {
	Logger: require("./src/logger.js"),
	Event: require("./src/event.js"),
	Statement: require("./src/statement.js"),
	Queue: require("./src/queue.js"),
	INFO: "INFO",
	DEBUG: "DEBUG",
	VERBOSE: "VERBOSE",
	VERYVERBOSE: "VERYVERBOSE",
	WARNING: "WARNING",
	ERROR: "ERROR"
}

module.exports = Logger;
