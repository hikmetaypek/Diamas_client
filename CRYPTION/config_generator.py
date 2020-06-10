# Base:
"""
[
	{
		"dir": "root",
		"file": "../data/root.dia",
		"visualdir": "",
		"key": [
			0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
			0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4
		],
		"type": ["archive_flag_lz4", "archive_flag_aes256"],
		"version": 5,
		"ignores": [
			"*.csv",
			"*error_lookup.pyc",
			"*test*.pyc"
		],
		"patches": {
			"stdlib\\": ""
		}
	}
	...
]
"""
# Beautifier: https://jsonformatter.curiousconcept.com

archives = {}

with open("pack_list.txt") as file:
	for line in file.readlines():
		dir = line.split("CEterPackManager::Instance().RegisterPack(\"")[1].split("\",")[0]
		dir = "../" + dir

		visualdir = line.split("\"")[3]
		if (visualdir == "*"):
			visualdir = ""
		else:
			visualdir += "/"

		archives[dir] = visualdir

template = """\
	{
		"dir": "PACK_NAME_HERE",
		"file": "PACK_DIR_HERE",
		"visualdir": "PACK_VDIR_HERE",
		"key": [
			0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
			0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4
		],
		"type": ["archive_flag_lz4", "archive_flag_aes256"],
		"version": 5
	},
"""

formattedData = ""
for k, v in archives.items():
	templateCopy = template
	templateCopy = templateCopy.replace("PACK_NAME_HERE", k.split("../data/")[1])
	templateCopy = templateCopy.replace("PACK_DIR_HERE", k + ".dia")
	templateCopy = templateCopy.replace("PACK_VDIR_HERE", v)

	formattedData += templateCopy

with open("config.json", "a") as file:
	file.write(formattedData)
