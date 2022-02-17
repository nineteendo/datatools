import json
options = {"foundIn": True}
def add_version(data, keyz):
	if isinstance(data, list):
		for value in data:
			add_version(value, keyz)
	elif isinstance(data, dict):
		for key, value in sorted(data.items()):
			if keyz == [] or keyz[0] == key:
				add_version(value, keyz[1:])
	elif keyz == []:
		keys.setdefault(data, []).append(id)

keys = {}
ids = ["1.0", "1.1", "1.2"]
source = {
"1.0": [1,2,3],
"1.1": [2,3,4,5],
"1.2": [2,4,5,6]
}

print("key", end = "")
if options["foundIn"]:
	print("	found in", end = "")
	for id in ids:
		add_version(source[id], [])
else:
	for id in ids:
		print("	" + id, end = "")
		add_version(source[id], [])
for key, value in keys.items():
	print("\n" + str(key), end = "")
	if options["foundIn"]:
		old_id = None
		for id in ids:
			if id in value:
				if old_id == None:
					print("	" + id + "-", end = "")
				old_id = id
			elif old_id != None:
				print(old_id, end = "")
				old_id = None
		if old_id != None:
			print("latest", end = "")
	else:
		for id in ids:
			if id in value:
				print("	X", end = "")
			else:
				print("	", end = "")