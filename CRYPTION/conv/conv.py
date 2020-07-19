#!/usr/bin/env python

def LoadTextConfigFile(filename):
	for line in open(filename, "r"):
		if line and line[0] != '#':
			yield line.strip().split("\t")

def ProcessNpcList(source_filename, dst_filename):
	with open(dst_filename, "wb+") as out_file:
		out_file.write("import chrmgr\n\n")

		for tokens in LoadTextConfigFile(source_filename):
			if not tokens[0].isdigit():
				continue

			vnum = int(tokens[0])
			if vnum:
				out_file.write("chrmgr.RegisterRaceName(%s, '%s')\n" % (vnum, tokens[1].strip()))
			else:
				out_file.write("chrmgr.RegisterRaceSrcName('%s', '%s')\n" % (tokens[1].strip(), tokens[2].strip()))

def ProcessGuildBuildingList(source_filename, dst_filename):
	TOKEN_VNUM = 0
	TOKEN_TYPE = 1
	TOKEN_NAME = 2
	TOKEN_LOCAL_NAME = 3
	NO_USE_TOKEN_SIZE_1 = 4
	NO_USE_TOKEN_SIZE_2 = 5
	NO_USE_TOKEN_SIZE_3 = 6
	NO_USE_TOKEN_SIZE_4 = 7
	TOKEN_X_ROT_LIMIT = 8
	TOKEN_Y_ROT_LIMIT = 9
	TOKEN_Z_ROT_LIMIT = 10
	TOKEN_PRICE = 11
	TOKEN_MATERIAL = 12
	TOKEN_NPC = 13
	TOKEN_GROUP = 14
	TOKEN_DEPEND_GROUP = 15
	TOKEN_ENABLE_FLAG = 16
	LIMIT_TOKEN_COUNT = 17

	ENABLE_FLAG_TYPE_NOT_USE = False
	ENABLE_FLAG_TYPE_USE = True
	ENABLE_FLAG_TYPE_USE_BUT_HIDE = 2

	# Sync these with the constants in root/uiGuild.py
	MATERIAL_STONE_INDEX = 0
	MATERIAL_LOG_INDEX = 1
	MATERIAL_PLYWOOD_INDEX = 2

	MATERIAL_STONE_ID = 90010
	MATERIAL_LOG_ID = 90011
	MATERIAL_PLYWOOD_ID = 90012

	with open(dst_filename, "wb+") as out_file:
		out_file.write("import uiGuild\n")
		out_file.write("uiGuild.BUILDING_DATA_LIST = [\n")

		register_str = ["import chrmgr"]

		line_index = 0
		for tokens in LoadTextConfigFile(source_filename):
			if not tokens[TOKEN_VNUM].isdigit():
				continue

			if len(tokens) < LIMIT_TOKEN_COUNT:
				print "Strange token count on line " + line_index
				continue

			if ENABLE_FLAG_TYPE_NOT_USE == int(tokens[TOKEN_ENABLE_FLAG]):
				continue

			vnum = int(tokens[TOKEN_VNUM])
			type = tokens[TOKEN_TYPE]
			name = tokens[TOKEN_NAME]
			localName = tokens[TOKEN_LOCAL_NAME]
			xRotLimit = int(tokens[TOKEN_X_ROT_LIMIT])
			yRotLimit = int(tokens[TOKEN_Y_ROT_LIMIT])
			zRotLimit = int(tokens[TOKEN_Z_ROT_LIMIT])
			price = tokens[TOKEN_PRICE]
			material = tokens[TOKEN_MATERIAL]

			folderName = ""
			if "HEADQUARTER" == type:
				folderName = "headquarter"
			elif "FACILITY" == type:
				folderName = "facility"
			elif "OBJECT" == type:
				folderName = "object"
			elif "WALL" == type:
				folderName = "fence"

			materialList = ["0", "0", "0"]
			if material:
				if material[0] == "\"":
					material = material[1:]
				if material[-1] == "\"":
					material = material[:-1]
				for one in material.split("/"):
					data = one.split(",")
					if 2 != len(data):
						continue
					itemID = int(data[0])
					count = data[1]

					if itemID == MATERIAL_STONE_ID:
						materialList[MATERIAL_STONE_INDEX] = count
					elif itemID == MATERIAL_LOG_ID:
						materialList[MATERIAL_LOG_INDEX] = count
					elif itemID == MATERIAL_PLYWOOD_ID:
						materialList[MATERIAL_PLYWOOD_INDEX] = count

			register_str.append("chrmgr.RegisterRaceSrcName('%s', '%s')" % (name, folderName))
			register_str.append("chrmgr.RegisterRaceName(%d, '%s')" % (vnum, name))

			appendingData = { "VNUM":vnum,
							  "TYPE":type,
							  "NAME":name,
							  "LOCAL_NAME":localName,
							  "X_ROT_LIMIT":xRotLimit,
							  "Y_ROT_LIMIT":yRotLimit,
							  "Z_ROT_LIMIT":zRotLimit,
							  "PRICE":price,
							  "MATERIAL":materialList,
							  "SHOW" : True }

			if ENABLE_FLAG_TYPE_USE_BUT_HIDE == int(tokens[TOKEN_ENABLE_FLAG]):
				appendingData["SHOW"] = False

			out_file.write("\t%s,\n" % str(appendingData))
			line_index += 1

		out_file.write("]\n")
		out_file.write("\n".join(register_str))