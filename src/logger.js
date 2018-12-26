const statement = require("./statement.js");
const event = require("./event.js");
const queue = require("./queue.js");

class Logger {
	constructor(config) {
		this.name = "Logger";
		let locations = {
			"node": "./log/node"
		}
		if (config) {
			if (config.name) {
				if (typeof config.name != "string") throw new TypeError(`Expected string, got ${typeof config.name} for config.name`);
				this.name = config.name;
			}
			if (config.locations) {
				if (typeof config.locations != "object") throw new TypeError(`Expected object, got ${typeof config.locations} for config.locations`);
				locations = config.locations;
			}
		}
		Object.keys(locations).forEach(function (name) {
			let location = locations[name];
			if (typeof location != "string") throw new TypeError(`Expected string, got ${typeof location} for location`);
			locations[name] = new queue(name, location);
		});
		this.locations = locations;
		return this;
	}

	queue(name) {
		if (typeof name != "string") throw new TypeError(`Expect string, got ${typeof name} for name parameter`);
		if (this.locations[name] == null) throw new TypeError(`Requested queue, ${name}, is nonexistent`);
		return this.locations[name];
	}
}

module.exports = Logger;
