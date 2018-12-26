const statement = require("./statement.js");

class Event {
	constructor() {
		if (arguments.length == 0) this.statementsVar = [];
		if (arguments.length == 1) this.statementsVar = [arguments[0]];
		if (arguments.length == 3) this.statementsVar = [new statement(arguments[0], arguments[1], arguments[2])];
	}

	get statements() {return this.statementsVar}
	set statements(statements) {this.statementsVar = statements}

	push() {
		if (arguments.length == 1) this.statements.push(arguments[0].statements);
		if (arguments.length == 3) this.statements.push(new statement(arguments[0], arguments[1], arguments[2]));
		return this;
	}
}

module.exports = Event;
