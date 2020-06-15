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
		errorMsg = "No file or directory ({0}) Type 2".format(filename)
		# dbg.TraceError(errorMsg)
		raise IOError(errorMsg)

	return data

def OpenVfsFile(filename):
	return cStringIO.StringIO(GetVfsFile(filename))

__builtin__.OpenVfsFile = OpenVfsFile

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

# exec & execfile
#oldExec = __builtin__.exec

def __execFileTrampoline(fileName, dict=None):
	ref = sys._getframe(1).f_code.co_filename

	import pack
	if not ref or not pack.ExistInPack(ref):
		errorMsg = "No such file or directory ({0}) Type 4 From ({1})".format(fileName, ref)
		dbg.TraceError(errorMsg)
		raise IOError(errorMsg)

	if not pack.ExistInPack(fileName):
		errorMsg = "No such file or directory ({0}) Type 4-2 From ({1})".format(fileName, ref)
		dbg.TraceError(errorMsg)
		raise IOError(errorMsg)

	data = GetVfsFile(fileName)

	if fileName.endswith(".pyc") or fileName.endswith(".pyo"):
		if data[:4] != imp.get_magic(): 
			raise ImportError("Invalid magic")

		code = marshal.loads(data[8:]) 
	else:
		code = compile(data, fileName, "exec")

	exec code in dict

__builtin__.execfile = __execFileTrampoline

#dbg.LogBox("3")

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
