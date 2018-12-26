class Statement {
	constructor(verbosity, tag, message) {
		this.timestampVar = new Date();
		this.verbosityVar = (verbosity != null && typeof verbosity == "string") ? verbosity : "INFO";
		this.tagVar = (tag != null && typeof tag == "string") ? tag : "TAG";
		this.messageVar = (message != null && typeof verbosity == "string") ? message : "";
		return this;
	}

	get timestamp() {return this.timestampVar}
	get verbosity() {return this.verbosityVar}
	get tag() {return this.tagVar}
	get message() {return this.messageVar}

	set timestamp(timestamp) {this.timestampVar = timestamp}
	set verbosity(verbosity) {this.verbosityVar = verbosity}
	set tag(tag) {this.tagVar = tag}
	set message(message) {this.messageVar = message}
}

module.exports = Statement;
