import os
import sys
import subprocess
import shutil

from conv.conv import ProcessNpcList, ProcessGuildBuildingList

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def ProcessLocale(lang, protoPath):
	curPath = os.getcwd()
	with cd("../../share/conf"):
		subprocess.check_call(["dump_proto", str(lang)])
		shutil.copyfile("item_proto", curPath+"/"+protoPath+"item_proto")
		shutil.copyfile("mob_proto", curPath+"/"+protoPath+"mob_proto")

if __name__ == '__main__':
	# Process special files
	ProcessNpcList("source/root/NpcList.csv", "source/root/NpcList.py")
	ProcessGuildBuildingList("../../Diamas/share/conf/object_proto.csv", "source/root/GuildBuildingList.py")