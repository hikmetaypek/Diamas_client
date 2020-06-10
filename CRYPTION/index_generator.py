import os

target = "../data/"
output = "../data/Index"

# Touch
with open(output, "a"):
	os.utime(output, None)

# Write new content
with open(output, "w") as out:
	for f in os.listdir(target):
		if (os.path.isfile(os.path.join(target, f)) and f != "Index" and os.path.splitext(f)[1] == ".dia"):
			out.write("%s\n" % f)
