import sys
import imp
import marshal
import cStringIO
import __builtin__
import dbg

#dbg.LogBox("1")

sys.path.append("stdlib")

class TraceFile:
	def write(self, msg):
		dbg.Tracen(msg)

class TraceErrorFile:
	def write(self, msg):
		dbg.TraceError(msg)
		dbg.RegisterExceptionString(msg)

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

def GetVfsFile(filename):
	import pack
	data = pack.Get(filename)
	if data == None:
		raise IOError("No file or directory ({0})".format(filename))

	return data

def OpenVfsFile(filename):
	return cStringIO.StringIO(GetVfsFile(filename))

__builtin__.OpenVfsFile = OpenVfsFile

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

def execfile(fileName, dict=None):
	data = GetVfsFile(fileName)

	if fileName.endswith(".pyc") or fileName.endswith(".pyo"):
		if data[:4] != imp.get_magic(): 
			raise ImportError("Invalid magic")

		code = marshal.loads(data[8:]) 
	else:
		code = compile(data, fileName, "exec")

	exec code in dict

__builtin__.execfile = execfile

#dbg.LogBox("3")


loginMark = "-cs"

"""
import os
if not os.path.isfile("locale.cfg"):
	localeConfig = open("locale.cfg", "w")
	localeConfig.write("0 0 de")
	localeConfig.close()
	app.ForceSetLocale("de", "locale/de")

if not os.path.isfile("mylang.cfg"):
	localeConfig = open("mylang.cfg", "w")
	localeConfig.write("de")
	localeConfig.close()
"""

#dbg.LogBox("4")

def GetExceptionString(excTitle):
	# dbg.LogBox("exc")

	(excType, excMsg, excTraceBack)=sys.exc_info()

	dbg.LogBox("%s-%s-%s" % (str(excType),str(excMsg),str(excTraceBack)))

	excText=""

	import traceback
	traceLineList=traceback.extract_tb(excTraceBack)

	for traceLine in traceLineList:
		if traceLine[3]:
			excText+="%s(line:%d) %s - %s" % (traceLine[0], traceLine[1], traceLine[2], traceLine[3])
		else:
			excText+="%s(line:%d) %s"  % (traceLine[0], traceLine[1], traceLine[2])

		excText+="\n"
	
	excText+="%s - %s:%s" % (excTitle, excType, excMsg)

	return excText

def ShowException(excTitle):
	excText=GetExceptionString(excTitle)
	dbg.TraceError(excText)
	AbortApp()

	return 0

#dbg.LogBox("5")

def RunMainScript(name):

#	dbg.LogBox("runmain")

	try:
#		dbg.LogBox("rm1")

		import __main__
#		dbg.LogBox("rm2")

		execfile(name, __main__.__dict__)
#		dbg.LogBox("rm2")

	except RuntimeError, msg:
#		dbg.LogBox(str(msg), "rm-runtime")

		msg = str(msg)

		import localeInfo
		if localeInfo.error:
			msg = localeInfo.error.get(msg, msg)

		dbg.LogBox(msg)
		dbg.TraceError(msg)
		AbortApp()

	except:
#		dbg.LogBox("rm-exception")

		msg = GetExceptionString("Run")
		dbg.LogBox(msg)
		dbg.TraceError(msg)
		AbortApp()

RunMainScript("prototype.py")
