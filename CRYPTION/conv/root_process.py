from __future__ import print_function

import sys
import os
import glob
import cStringIO

from preprocess import preprocess

# TODO(tim): Make this go away
import source_writer
import conv

def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)

def __CythonizeSources(nthreads=0):
	# Add Cython root directory to our import path
	# /client/data/conv/<file> -> /extern/Py2Lib/Cython
	root = os.path.realpath(__file__)
	for i in xrange(4):
		root, _ = os.path.split(root)
	warning(root)

	sys.path.insert(0, os.path.join(root, "Diamas", "extern", "Py2Lib"))

	from Cython.Build import cythonize

	options = {
		"global_options": {
			# Needed for locale constants (and __DEBUG__, etc.)
			"error_on_unknown_names": False,
		},
	}

	sys.path.append("source/cyTemp")
	# This gets us a list of distutils Extension objects
	
	exts = cythonize("source/cyTemp/*.pyx", nthreads=nthreads, language="c++", **options)

	module_names = []
	for m in exts:
		for source in m.sources:
			file = os.path.split(source)[1]
			module_names.append(os.path.splitext(file)[0])

	source_writer.run(module_names, "rootlib")

def Main(language):
	sources = glob.glob("source\\root\\*.py")
	sources.remove("system_python.py")

	defines = {
		"LANGUAGE": language,
	}

	for src in sources:
		# Remove all directories from the path.
		# We don't support packages anyway.
		dst = os.path.split(src)[1]

		if language == "cython":
			# .py files cannot use Cython features
			dst += "x"

		of = cStringIO.StringIO()
		preprocess(src,
		           of,
		           defines,
		           True)

		path = os.path.join("source/cyTemp", dst)

		try:
			with open(path, "r") as f:
				data = f.read()
		except IOError:
			data = None

		if not data or data != of.getvalue():
			with open(path, "wb") as f:
				f.write(of.getvalue())

	if language == "cython":
		# TODO(tim): Auto-detect CPU count
		__CythonizeSources(3)
		
	

if __name__ == "__main__":
	# usage: <language: python|cython>
	Main(*sys.argv[1:])