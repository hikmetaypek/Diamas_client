import os

target = "../pack/"
output = "../pack/Index"

# Touch
with open(output, "a"):
	os.utime(output, None)

# Write new content
with open(output, "w") as out:
	for f in os.listdir(target):
		if (os.path.isfile(os.path.join(target, f)) and f != "Index" and os.path.splitext(f)[1] == ".rh2"):
			out.write("%s\n" % f)
