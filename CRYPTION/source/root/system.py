import sys
import imp
import marshal
import cStringIO
import __builtin__
import dbg

# dbg.LogBox("1")

sys.path.append("stdlib")

class TraceFile:
	def write(self, msg):
		dbg.Tracen(msg)

class TraceErrorFile:
	def write(self, msg):
		dbg.TraceError(msg)

class LogBoxFile:
	def __init__(self):
		self.stderrSave = sys.stderr
		self.msg = ""

	def __del__(self):
		self.restore()

	def restore(self):
		sys.stderr = self.stderrSave

	def write(self, msg):
		self.msg = self.msg + msg

	def show(self):
		dbg.LogBox(self.msg,"Error")

# dbg.LogBox("2")

sys.stdout = TraceFile()
sys.stderr = TraceErrorFile()

def AbortApp():
	import app
	app.Abort()

from libcpp.string cimport string

import rootlib

cdef extern from "pack.h":
	string GetPackFileData(string filename)

cdef bytes GetVfsFile(string filename):
	cdef string data = GetPackFileData(filename)
	if data.empty():
		raise IOError("No file or directory ({0})".format(filename))

	return <bytes>data

cdef object OpenVfsFile(string filename):
	return cStringIO.StringIO(GetVfsFile(filename))

class CythonModuleLoader(object):
	def load_module(self, fullname):
		return rootlib.moduleImport(fullname)

class CythonModuleFinder(object):
	def find_module(self, fullname, path=None):
		if not rootlib.isExist(fullname):
			return None

		return CythonModuleLoader()

sys.meta_path.append(CythonModuleFinder())

# dbg.LogBox("3")

# builtin_open
oldOpen = __builtin__.open

def __openTrampoline(*args,**kwargs):
	foundExts = False
	whiteListedExts = [".cfg", ".txt", ".eig", ".inf"]
	for i in whiteListedExts:
		if i in args[0]:
			foundExts = True
			break

	if not foundExts and "." in args[0]:
		errorMsg = "No such file or directory ({0}) Type 3".format(args[0])
		dbg.TraceError(errorMsg)
		raise IOError(errorMsg)

	r = oldOpen(*args,**kwargs)
	return r

__builtin__.open = __openTrampoline

# dbg.LogBox("4")

# EterPack methods
class EterPackModuleLoader(object):
	def __init__(self, filename, code, is_package):
		self.filename = filename
		self.code = code
		self.is_package = is_package

	def load_module(self, fullname):
		mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
		mod.__file__ = self.filename
		mod.__loader__ = self

		if self.is_package:
			mod.__path__ = []
			mod.__package__ = fullname
		else:
			mod.__package__ = fullname.rpartition('.')[0]

		exec(self.code, mod.__dict__)
		return mod

class EterPackModuleFinder(object):
	def find_module(self, fullname, path=None):
		if imp.is_builtin(fullname):
			return None

		path = fullname.replace('.', '/')

		loader = self.__MakeLoader(path + ".py", False, False)
		if loader:
			dbg.Tracen("Found and loaded module {0}".format(fullname))
			return loader

		loader = self.__MakeLoader(path + ".pyc", True, False)
		if loader:
			dbg.Tracen("Found and loaded module {0}".format(fullname))
			return loader

		loader = self.__MakeLoader(path + "/__init__.py", False, True)
		if loader:
			dbg.Tracen("Found and loaded package {0}".format(fullname))
			return loader

		loader = self.__MakeLoader(path + "/__init__.pyc", True, True)
		if loader:
			dbg.Tracen("Found and loaded package {0}".format(fullname))
			return loader

		dbg.Tracen("Failed to find {0}".format(fullname))
		return None

	def __MakeLoader(self, filename, is_compiled, is_package):
		try:
			data = GetVfsFile(filename)
		except IOError:
			return None

		if is_compiled:
			if data[:4] != imp.get_magic():
				raise ImportError("Bad magic")

			code = marshal.loads(data[8:])
		else:
			code = compile(data, filename, "exec")

		return EterPackModuleLoader(filename, code, is_package)

sys.meta_path.append(EterPackModuleFinder())

# dbg.LogBox("5")

# exec & execfile
#oldExec = __builtin__.exec

def __execFileTrampoline(fileName, dict=None):
	data = GetVfsFile(fileName)

	if fileName.endswith(".pyc") or fileName.endswith(".pyo"):
		if data[:4] != imp.get_magic(): 
			raise ImportError("Invalid magic")

		code = marshal.loads(data[8:]) 
	else:
		code = compile(data, fileName, "exec")

	exec code in dict

__builtin__.execfile = __execFileTrampoline

# dbg.LogBox("7")

import Prototype
