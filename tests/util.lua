#!/usr/bin/env lua

require("hexdump")

-- I/O utilities
function printf(fmt, ...)
	io.write(string.format(fmt, ...))
end

-- simple argparse
function arg_verify(arg, ...)
	for i,v in pairs{...} do
		if arg == v then return true end
	end
end

function arg_forward(v, position, param_count)
	forward_valid = position + param_count <= #arg
	if not forward_valid then
		printf("error: arg %s requires %d parameter(s)\n", v, param_count)
		os.exit(1)
	end
	return true
end

-- display outputs
function display_help()
	printf("usage: %s %s [OPTIONS]..\n\n", arg[-1], arg[0])
	printf("General:\n")
	printf("  --help, -h, -?\tDisplays this help output\n")
	printf("  --version, -v\t\tDisplays program information and copyright info\n")
	printf("\nFlags:\n")
	printf("  -e, --encode\t\tRun in encode mode (default)\n")
	printf("  -d, --decode\t\tRun in decode mode\n")
	printf("  -p\t\t\tPrettify output\n")
	printf("  --debug\t\tPrint debug output and exit\n")
	printf("\nEncode params:\n")
	printf("  -x\t\t\tObject type (STATEMENT or EVENT)\n")
	printf("  -b\t\t\tVerbosity (INFO, DEBUG, etc.)\n")
	printf("  -p\t\t\tParent ID\n")
	printf("  -t\t\t\tTimestamp\n")
	printf("  -m\t\t\tMessage\n")
	os.exit()
end

function display_short()
	printf("usage: %s %s [OPTIONS]..\n", arg[-1], arg[0])
	printf("Pass --help for more info\n")
	os.exit()
end

function display_version()
	printf("lognestmonster Lua utils Copyright (c) 2020 Joshua 'joshuas3' Stockin\n")
	printf("<https://joshstock.in> <https://github.com/JoshuaS3/lognestmonster>\n")
	printf("\n")
	printf("This software's source is licensed and distributed under the terms of\n")
	printf("the MIT License. See the attached LICENSE for more information.\n")
	os.exit()
end

if #arg == 0 then display_short() end

VERBOSITY = {
	INFO = 0,
	DEBUG = 1,
	VERBOSE = 2,
	VERYVERBOSE = 3,
	WARNING = 4,
	ERROR = 5
}

SETTINGS = {
	MODE = "ENCODE",
	ENCODE = {
		TYPE = "STATEMENT",
		EVENT = {
			PARENT_ID = 0,
			EVENT_ID = 1,
			TAG = ""
		},
		STATEMENT = {
			VERBOSITY = "INFO",
			PARENT_ID = 0,
			TIMESTAMP = 0,
			MESSAGE = ""
		}
	},
	DECODE = {
		DUMP = ""
	},
	PRETTIFY = false,
	DEBUG = false
}

i = 1
while i <= #arg do
	v = arg[i]
	if arg_verify(v, "--help", "-h", "-?", "help", "h", "?") then
		display_help()
	elseif arg_verify(v, "--version", "-v") then
		display_version()
	elseif arg_verify(v, "-d", "--decode") then
		SETTINGS.MODE = "DECODE"
	elseif arg_verify(v, "-e", "--encode") then
		SETTINGS.MODE = "ENCODE"
	elseif arg_verify(v, "-p") then
		SETTINGS.PRETTIFY = true
	elseif arg_verify(v, "-x") then
		if SETTINGS.MODE ~= "ENCODE" then
			printf("error: -x can only be passed in ENCODE mode\n")
			os.exit(1)
		end
		arg_forward(v, i, 1)
		val = arg[i + 1]
		if val ~= "STATEMENT" and val ~= "EVENT" then
			printf("error: -x should be 'STATEMENT' or 'EVENT'\n")
			os.exit(1)
		end
		SETTINGS.ENCODE.TYPE = val
		i = i + 1
	elseif arg_verify(v, "-b") then
		if SETTINGS.MODE ~= "ENCODE" then
			printf("error: -b can only be passed in ENCODE mode\n")
			os.exit(1)
		end
		arg_forward(v, i, 1)
		val = arg[i + 1]
		if VERBOSITY[val] == nil then
			printf("error: invalid verbosity (-b): %s\n", val)
			os.exit(1)
		end
		SETTINGS.ENCODE.VERBOSITY = val
		i = i + 1
	elseif arg_verify(v, "--debug") then
		SETTINGS.DEBUG = true
	else
		display_short()
	end
	i = i + 1
end

if SETTINGS.DEBUG then
	printf("Encoding type: %s\n", SETTINGS.ENCODE.TYPE)
	printf("")
	os.exit(0)
end
