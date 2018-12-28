const statement = require("./statement.js");
const event = require("./event.js");

const FileHandler = require("./fileHandler.js");

class Queue {
	constructor(name, location, config) {
		if (typeof name != "string") throw new Error(`Expected string, got ${typeof name} for name`);
		if (typeof location != "string") throw new Error(`Expected string, got ${typeof location} for location`);
		this.name = name;
		this.timestamp = new Date();
		this.location = location;
		this.filename = this.location + "/" + this.timestamp.toISOString().replace(/\:/g, "-").replace(/\./g, "-") + ".log";
		this.queue = [];

		this.compact = false;
		this.fileStarted = false;
		
		if (config) {
			if (config.compact) {
				if (typeof config.compact != "boolean") throw new Error(`Expected boolean, got ${typeof config.compact} for config.compact`);
				this.compact = config.compact;
			}
		}

		FileHandler.AppendFile(this.filename, ""); // touch the file

		return this;
	}

	push() {
		if (arguments.length >= 3) this.queue.push(new statement(arguments[0], arguments[1], arguments[2]));
		else if (arguments.length > 0) {
			if (arguments[0] instanceof event) this.queue.push(arguments[0].statements); // object is an Event
			else if (arguments[0] instanceof statement) this.queue.push(arguments[0]); // object is a Statement
			else throw new TypeError("Expected an Event or Statement");
		} else throw new Error("Expected at least one argument");
		return this;
	}

	write() {
		let recursiveCompactFunction;
		if (this.compact) {
			recursiveCompactFunction = function(object) {
				if (Array.isArray(object)) {
					for (let i = 0; i < object.length; i++) {
						object[i] = recursiveCompactFunction(object[i]);
					}
					return object;
				} else {
					let fixed = {};
					fixed.tt = object.timestamp;
					fixed.v = object.verbosity;
					fixed.t = object.tag;
					fixed.m = object.message;
					return fixed;
				}
			}
		}

		if (arguments.length > 0) {
			let toWrite;
			if (arguments.length >= 3) toWrite = new statement(arguments[0], arguments[1], arguments[2]);
			else {
				if (arguments[0] instanceof event) toWrite = arguments[0].statements; // object is an Event
				else if (arguments[0] instanceof statement) toWrite = arguments[0]; // object is a Statement
				else throw new TypeError("Expected an Event or Statement");
			}

			if (this.compact) {
				toWrite = recursiveCompactFunction(toWrite);
			}

			let appendString = "";
			if (this.fileStarted) appendString += "\n";
			appendString += JSON.stringify(toWrite);
			if (!this.fileStarted) this.fileStarted = true;
			FileHandler.AppendFile(this.filename, appendString);
		} else {
			let queueLength = this.queue.length;
			if (queueLength > 0) {
				let appendString = "";
				let queue = this;
				let toWrite = this.queue;
				if (this.compact) {
					toWrite = recursiveCompactFunction(toWrite);
				}
				toWrite.forEach(function (item) {
					if (queue.fileStarted) appendString += "\n";
					appendString += JSON.stringify(item);
					if (!queue.fileStarted) queue.fileStarted = true;
				});
				this.queue = this.queue.slice(queueLength);
				FileHandler.AppendFile(this.filename, appendString);
			}
		}
		return this;
	}
}

module.exports = Queue;
