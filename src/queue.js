const statement = require("./statement.js");

class Queue {
	constructor(name, location) {
		this.name = name;
		this.location = location;
		this.queue = [];
		return this;
	}

	push() {
		if (arguments.length >= 3) {
			if (typeof arguments[0] == "string" && typeof arguments[1] == "string" && typeof arguments[2] == "string") {
				this.queue.push(new statement(arguments[0], arguments[1], arguments[2]));
			} else throw new Error("Expected 3 strings for Statement creation");
		} else if (arguments.length > 0) {
			if (arguments[0].statements) this.queue.push(arguments[0].statements); // object is an Event
			else if (arguments[0].timestamp) this.queue.push(arguments[0]); // object is a Statement
			else throw new Error("Expected an Event or Statement object");
		} else throw new Error("Expeted at least one argument");
		return this;
	}

	write() {
		return this;
	}
}

module.exports = Queue;
