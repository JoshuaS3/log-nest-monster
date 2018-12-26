const fs = require("fs");
const path = require("path");

class FileHandler {
	static RecursiveMkdir(file) {
		let paths = path.normalize(file).split(path.sep);
		let curPath = (path.isAbsolute(file)) ? "" : ".";
		for (var i = 0; i < paths.length; i++) {
			curPath += path.sep + paths[i];
			if (!fs.existsSync(curPath))
				fs.mkdirSync(curPath);
		}
	}
	static AppendFile(file, data) {
		if (typeof file != "string") throw new TypeError(`Expected string, got ${typeof file} for file`);
		if (typeof data != "string") throw new TypeError(`Expected string, got ${typeof data} for data`);
		if (!fs.existsSync(path.dirname(file))) {
			FileHandler.RecursiveMkdir(path.dirname(file));
			fs.appendFileSync(file, data);
		} else fs.appendFileSync(file, data);
	}
}

module.exports = FileHandler;
