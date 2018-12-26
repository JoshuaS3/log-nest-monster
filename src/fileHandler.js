const fs = require("fs");
const path = require("path");

class FileHandler {
	static RecursiveMkdir(file) {
		let currentFile = path.normalize(file);
		let pathWorks = false;
		let backToStart = false;
		if (!fs.existsSync(path.normalize(file))) {
			while (!pathWorks) {
				if (fs.existsSync(path.normalize(currentFile))) {
					pathWorks = true;
					while (!backToStart) {
						if (!fs.existsSync(path.dirname(currentFile))) {
							fs.mkdirSync(path.dirname(currentFile));
						}
						if (fs.existsSync(path.normalize(file))) {
							backToStart = true;
							break;
						}
						currentFile = currentFile.slice(0, -3);
					}
					break;
				} else {
					currentFile += "\\.."
				}
			}
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
