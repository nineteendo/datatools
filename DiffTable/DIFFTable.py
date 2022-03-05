import sys, datetime
from traceback import format_exc
from json import load
from os import makedirs, listdir, system, getcwd, sep
from os.path import isdir, isfile, realpath, join as osjoin, dirname, relpath, basename, splitext
options = {
	"confirmPath": True,
	"DEBUG_MODE": True,
	"enteredPath": False,
	"foundIn": True
}

# Print & log error
def error_message(string):
	if options["DEBUG_MODE"]:
		string += "\n" + format_exc()
	
	fail.write(string + "\n")
	fail.flush()
	print("\033[91m" + string + "\033[0m")

# Print & log warning
def warning_message(string):
	fail.write("\t" + string + "\n")
	fail.flush()
	print("\33[93m" + string + "\33[0m")

# Print in blue text
def blue_print(text):
	print("\033[94m" + text + "\033[0m")

# Print in green text
def green_print(text):
	print("\033[32m" + text + "\033[0m")

# Input in bold text
def bold_input(text):
	return input("\033[1m" + text + "\033[0m: ")

# Input hybrid path
def path_input(text, full_path = True):
	string = ""
	newstring = bold_input(text)
	while newstring or string == "":
		if options["enteredPath"]:
			string = newstring
		else:
			string = ""
			quoted = 0
			escaped = False
			tempstring = ""
			for char in newstring:
				if escaped:
					if quoted != 1 and char == "'" or quoted != 2 and char == '"' or quoted == 0 and char in "\\ ":
						string += tempstring + char
					else:
						string += tempstring + "\\" + char
					tempstring = ""
					escaped = False
				elif char == "\\":
					escaped = True
				elif quoted != 2 and char == "'":
					quoted = 1 - quoted
				elif quoted != 1 and char == '"':
					quoted = 2 - quoted
				elif quoted != 0 or char != " ":
					string += tempstring + char
					tempstring = ""
				else:
					tempstring += " "
		if string == "":
			newstring = bold_input("\033[91mEnter a path")
		else:
			newstring = ""
			if full_path:
				string = realpath(string)
			if options["confirmPath"]:
				newstring = bold_input("Confirm \033[100m" + string)

	return string

def add_version(data, keyz, start, doublepoint):
	if isinstance(data, list):
		for value in data:
			add_version(value, keyz, start, doublepoint)
	elif isinstance(data, dict):
		add_dict(data, keyz, start, doublepoint)
	elif keyz == []:
		keys.setdefault(start + "	" + repr(data), []).append(id)

def add_dict(data, keyz, start, doublepoint):
	if keyz:
		check, dict_key = keyz[0]
		if check in data:
			if dict_key:
				add_dict(data, keyz[1:], start + repr(data[check]) + "	", "")
			else:
				add_version(data[check], keyz[1:], start, "")
	else:
		for key, value in sorted(data.items()):
			add_version(value, [], start + doublepoint + repr(key), ": ")

try:
	system("")
	if getattr(sys, "frozen", False):
		application_path = dirname(sys.executable)
	else:
		application_path = sys.path[0]

	fail = open(osjoin(application_path, "fail.txt"), "w")
	if sys.version_info[:2] < (3, 9):
		raise RuntimeError("Must be using Python 3.9")
	
	print("\033[95m\033[1mDiffTable v1.1.0\n(C) 2022 by Nineteendo\033[0m\n")
	try:
		newoptions = load(open(osjoin(application_path, "options.json"), "rb"))
		for key in options:
			if key in newoptions:
				if type(options[key]) == type(newoptions[key]):
					options[key] = newoptions[key]
				elif isinstance(options[key], tuple) and isinstance(newoptions[key], list):
					options[key] = tuple([str(i).lower() for i in newoptions[key]])
				elif key == "Indent" and type(newoptions[key]) in [int, type(None)]:
					options[key] = newoptions[key]
	except Exception as e:
		error_message(type(e).__name__ + " in options.json: " + str(e))

	blue_print("Working directory: " + getcwd())
	path = path_input("Enter directory")
	sub_path = path_input("Enter sub path", False)
	json_keys = []
	length = 0
	for i in range(0, int(bold_input("How many json_keys"))):
		key = bold_input("Key")
		if "" == bold_input("Dict Key"):
			json_keys.append((key, False))
		else:
			json_keys.append((key, True))
			length += 1

	file = open(osjoin(application_path, "changelog.tsv"), "w")
	file.write(length * "ID	" + "path	key")
	if options["foundIn"]:
		file.write("	found in")

	keys = {}
	ids = []
	for id in sorted(sorted(listdir(path)), key = lambda key : len(key)):
		try:
			add_version(load(open(osjoin(path, id, sub_path), "r")), json_keys, "", "")
			ids.append(id)
			if not options["foundIn"]:
				file.write("	" + id)
		except Exception as e:
			warning_message(type(e).__name__ + " : " + str(e))

	for key, value in keys.items():
		file.write("\n" + str(key))
		if options["foundIn"]:
			old_id = None
			first_id = None
			seperator = "	"
			for id in ids:
				if id in value:
					if old_id == None:
						first_id = id
						file.write(seperator + id)
						seperator = " & "
					old_id = id
				elif old_id != None:
					if first_id != old_id:
						file.write(" - " + old_id)
					old_id = None
			if old_id != None:
				file.write(" - present")
		else:
			for id in ids:
				counted = value.count(id)
				if counted:
					file.write("	" + str(counted))
				else:
					file.write("	")
	file.close()
	print("wrote changelog.tsv")
except BaseException as e:
	warning_message(type(e).__name__ + " : " + str(e))

# Close log
fail.close()