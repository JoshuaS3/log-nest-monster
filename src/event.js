const statement = require("./statement.js");

class Event {
	constructor() {
		if (arguments.length == 0) this.statements = [];
		else if (arguments.length == 1) {
			if (!arguments[0].timestamp && !arguments[0].statements) throw new Error("Expected an Event or Statement object");
			this.statements = [arguments[0]];
		} else if (arguments.length == 3) {
			if (typeof arguments[0] != "string" || typeof arguments[1] != "string" || typeof arguments[2] != "string") {
				throw new Error("Expected 3 strings for Statement creation")
			};
			this.statements = [new statement(arguments[0], arguments[1], arguments[2])];
		}
	}

	push() {
		if (arguments.length == 1) {
			if (arguments[0].statements) this.statements.push(arguments[0].statements); // object is an Event
			else this.statements.push(arguments[0]); // object is a Statement
		}
		if (arguments.length == 3) this.statements.push(new statement(arguments[0], arguments[1], arguments[2]));
		return this;
	}
}

module.exports = Event;
