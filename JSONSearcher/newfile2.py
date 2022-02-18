from os import makedirs, listdir, system, getcwd
from os.path import isdir, isfile, realpath, join as osjoin, dirname, relpath, basename, splitext

options = {"enteredPath": False, "confirmPath": True}

# Input in bold text
def bold_input(text):
	return input("\033[1m%s\033[0m: " % text)

# Input hybrid path
def path_input(text):
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
			string = realpath(string)
			if options["confirmPath"]:
				newstring = bold_input("Confirm \033[100m" + string)

	return string

def search(path):
	if isfile(path):
		try:
			counted = open(path, "r").read().count(find)
			if counted:
				print(path, counted)
		except Exception:
			pass
	elif isdir(path):
		for file in listdir(path):
			search(osjoin(path, file))

find = bold_input("Find")
search(path_input("Enter path"))