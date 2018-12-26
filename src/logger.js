const statement = require("./statement.js");
const event = require("./event.js")

class Logger {
	constructor(config) {
		this.nameVar = "Logger";
		this.locationsVar = {
			"node": "./log/node"
		}
		if (config) {
			if (config.name) {
				if (typeof config.name != "string") throw new Error(`Expected string, got ${typeof config.name} for config.name`);
				this.name = config.name;
			}
			if (config.locations) {
				if (typeof config.locations != "object") throw new Error(`Expected object, got ${typeof config.locations} for config.locations`);
				this.locations = config.locations;
			}
		}
		return this;
	}

	get name() {return this.nameVar}
	get locations() {return this.locationsVar}

	set name(name) {this.nameVar = name}
	set locations(newLocation) {this.addLocation(newLocation)}

	addLocation(name, location) {
		this.locationsVar[name] = location;
		return this;
	}

	push() {
		return this;
	}

	queue() {
		return this;
	}

	write() {
		return this;
	}
}

module.exports = Logger;
