import sys
from time import sleep
from shutil import copyfile
from traceback import format_exc
from json import load, dump
from os import makedirs, listdir, system, getcwd, sep, stat
from os.path import isdir, isfile, realpath, join as osjoin, dirname, relpath, basename, splitext
options = {
	"DEBUG_MODE": False,
	"files": {}
}

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
				for dst in childs:
					copyfile(file, dst)
					blue_print("wrote " + dst)
				
				times[file] = time
				dump(times, open(osjoin(application_path, ".times.json"), "w"))
		sleep(10)
except BaseException as e:
	error_message(type(e).__name__ + " : " + str(e))