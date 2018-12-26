class Statement {
	constructor(verbosity, tag, message) {
		this.timestamp = new Date();
		this.verbosity = (verbosity != null && typeof verbosity == "string") ? verbosity : "INFO";
		this.tag = (tag != null && typeof tag == "string") ? tag : "TAG";
		this.message = (message != null && typeof verbosity == "string") ? message : "";
		return this;
	}
}

module.exports = Statement;
