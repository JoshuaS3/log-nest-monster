const statement = require("./statement.js");
const event = require("./event.js");
const queue = require("./queue.js");

class Logger {
	constructor(config) {
		this.name = "Logger";
		this.locations = {
			"node": "./log/node"
		}
		if (config) {
			if (config.name) {
				if (typeof config.name != "string") throw new Error(`Expected string, got ${typeof config.name} for config.name`);
				this.name = config.name;
			}
			if (config.locations) {
				if (typeof config.locations != "object") throw new Error(`Expected object, got ${typeof config.locations} for config.locations`);
				let locations = {};
				Object.keys(config.locations).forEach(function (name) {
					if (typeof name != "string") throw new Error(`Expected string, got ${typeof name} for config.locations key`);
					let location = config.locations[name];
					if (typeof location != "string") throw new Error(`Expected string, got ${typeof location} for config.locations value`);
					locations[name] = new queue(name, location);
				});
				this.locations = locations;
			}
		}
		return this;
	}

	queue(name) {
		if (typeof name != "string") throw new Error(`Expect string, got ${typeof name} for name parameter`);
		if (this.location[name] == null) throw new Error(`Requested queue, ${name}, is nonexistent`);
		return this.locations[name];
	}
}

module.exports = Logger;
