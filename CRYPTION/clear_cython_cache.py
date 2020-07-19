import os

os.chdir("source/cyTemp")

for f in os.listdir("."):
	name, exts = os.path.splitext(f)
	if (f != "_dummy.cpp" and exts in [".cpp", ".pyx"]):
		os.remove(f)
