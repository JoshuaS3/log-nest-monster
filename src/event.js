const statement = require("./statement.js");

class Event {
	constructor() {
		this.statements = [];
		this.push(arguments);
		return this;
	}

	push() {
		if (arguments.length == 1) {
			if (arguments[0].statements) this.statements.push(arguments[0].statements); // object is an Event
			else this.statements.push(arguments[0]); // object is a Statement
		}
		else if (arguments.length == 3) this.statements.push(new statement(arguments[0], arguments[1], arguments[2]));
		else throw new Error("Expected 1 or 3 arguments");
		return this;
	}
}

module.exports = Event;
