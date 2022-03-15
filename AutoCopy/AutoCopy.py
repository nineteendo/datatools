import sys
from time import sleep
from traceback import format_exc
from json import load, dump
from os import system, stat, makedirs
from os.path import isdir, isfile, join as osjoin, dirname

# Default options
options = {
	"cooldown": 9,
	"DEBUG_MODE": False,
	"files": {}
}

# Default times edited
times = {}

# Print & log error
def error_message(string):
	if options["DEBUG_MODE"]:
		string += "\n" + format_exc()
	
	fail.write(string + "\n")
	fail.flush()
	print("\033[91m" + string + "\033[0m")

# Print in blue text
def blue_print(text):
	print("\033[94m" + text + "\033[0m")

try:
	system("")
	if getattr(sys, "frozen", False):
		application_path = dirname(sys.executable)
	else:
		application_path = sys.path[0]

	fail = open(osjoin(application_path, "fail.txt"), "w")
	if sys.version_info[:2] < (3, 9):
		raise RuntimeError("Must be using Python 3.9")
	
	print("\033[95m\033[1mAutoCopy v1.1.0\n(C) 2022 by Nineteendo\033[0m\n")
	try:
		newoptions = load(open(osjoin(application_path, "options.json"), "rb"))
		for key in options:
			if key in newoptions and type(options[key]) == type(newoptions[key]):
				options[key] = newoptions[key]
	except Exception as e:
		error_message(type(e).__name__ + " in options.json: " + str(e))

	cooldown = options["cooldown"]
	try:
		for key, value in load(open(osjoin(application_path, ".times.json"), "rb")).items():
			if isinstance(value, float):
				times[key] = value
	except Exception as e:
		error_message(type(e).__name__ + " in .times.json: " + str(e))
	
	while True:
		for file, childs in options["files"].items():
			time = stat(file).st_mtime
			if not file in times or time != times[file]:
				#check = checksum(file)
				data = open(file, "rb").read()
				for dst, replaces in childs.items():
					newdata = data
					for key, value in replaces.items():
						newdata = newdata.replace(key.encode(), value.encode())
					if isfile(dst):
						if hash(open(dst, "rb").read()) != hash(newdata):
							open(dst, "wb").write(newdata)
							blue_print("wrote " + dst)
					elif not isdir(dst):
						makedirs(dirname(dst), exist_ok = True)
						open(dst, "wb").write(newdata)
						blue_print("wrote " + dst)
				
				times[file] = time
				dump(times, open(osjoin(application_path, ".times.json"), "w"))
		sleep(1)
		sleep(cooldown)
except BaseException as e:
	error_message(type(e).__name__ + " : " + str(e))