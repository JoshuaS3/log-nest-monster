const statement = require("./statement.js");
const event = require("./event.js");

const FileHandler = require("./fileHandler.js");

class Queue {
	constructor(name, location) {
		this.name = name;
		this.timestamp = new Date();
		this.location = location;
		this.filename = this.location + "/" + this.timestamp.toISOString().replace(/\:/g, "-").replace(/\./g, "-") + ".log";
		this.queue = [];

		FileHandler.AppendFile(this.filename, "");

		return this;
	}

	push() {
		if (arguments.length >= 3) this.queue.push(new statement(arguments[0], arguments[1], arguments[2]));
		else if (arguments.length > 0) {
			if (arguments[0] instanceof event) this.queue.push(arguments[0].statements); // object is an Event
			else if (arguments[0] instanceof statement) this.queue.push(arguments[0]); // object is a Statement
			else throw new TypeError("Expected an Event or Statement");
		} else throw new Error("Expeted at least one argument");
		return this;
	}

	write() {
		let queueLength = this.queue.length;
		let appendString = ""
		this.queue.forEach(function (item) {
			appendString += JSON.stringify(item) + "\n";
		});
		this.queue = this.queue.slice(queueLength);
		FileHandler.AppendFile(this.filename, appendString);
		return this;
	}
}

module.exports = Queue;
