const Statement = require("./statement.js");

class Event {
	constructor() {
		this.statements = [];
		if (arguments.length > 0) this.push(arguments[0], arguments[1], arguments[2]);
		return this;
	}

	push() {
		if (arguments.length == 1) {
			if (arguments[0] instanceof Event && arguments[0] != this) this.statements.push(arguments[0].statements);
			else if (arguments[0] instanceof Statement) this.Statements.push(arguments[0]);
			else throw new TypeError("Expected an Event or Statement");
		}
		else if (arguments.length == 3) this.statements.push(new Statement(arguments[0], arguments[1], arguments[2]));
		else throw new Error("Expected 1 or 3 arguments");
		return this;
	}
}

module.exports = Event;
