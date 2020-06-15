#!/usr/local/bin/python

from urllib import urlopen
from datetime import date
import sys
import os
import zlib
import getopt
import csv
import zipfile

#
# Utility functions
#

def FindFilesByExt(path, ext):
	ext = ext.lower()

	for root, dirs, files in os.walk(path):
		for name in files:
			if name[-len(ext):].lower() == ext:
				yield os.path.join(root, name)

def GetFileCrc32(filename):
    crc = 0
    for line in open(filename, "rb"):
        crc = zlib.crc32(line, crc)

    return "%x" % (crc & 0xffffffff)

def FormatName(filename):
	if filename[:2] == ".\\":
		filename = filename[2:]
	
	return filename.replace("\\", "/")

def GetLastModifiedTime(filename):
	# http://support.microsoft.com/kb/167296
	# How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME
	EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
	HUNDREDS_OF_NANOSECONDS = 10000000
	
	return EPOCH_AS_FILETIME + long(os.path.getmtime(filename)) * HUNDREDS_OF_NANOSECONDS

#
# Real code
#

class Patch:
	def __init__(self):
		self.name = None
		self.patch_url = None
		
		# Patch file list
		self.file_dict = dict()
		self.file_list = None
		
	def SetName(self, name):
		self.name = name
	
	def SetPatchUrl(self, url):
		self.patch_url = url
	
	def AddFilesFromPatchUrl(self):
		for line in urlopen(self.patch_url):
			line = line.split()
			print line
			line[4] = FormatName(line[4])
			self.file_dict[line[4].lower()] = line
	
	def AddFile(self, filename):
		filename = FormatName(filename)
		mtime = GetLastModifiedTime(filename)

		#
		# Format is as following:
		# unpacked_crc unpacked_size low_last_edit high_last_edit path
		#

		self.file_dict[filename.lower()] = [GetFileCrc32(filename),
							"%d" % (os.path.getsize(filename)),
							"%d" % (mtime >> 32),
							"%d" % (mtime & 0xffffffff), filename]
							
		# Sorted list no longer contains all files. Invalidate it.
		self.file_list = None
	
	def GetCrcList(self):
		self.__SortFileList()
		
		output = ""
		for entry in self.file_list:
			output += (" ".join(entry) + "\n")
			
		return output

	def __SortFileList(self):
		if not self.file_list:
			self.file_list = [self.file_dict[key] for key in self.file_dict]
			self.file_list.sort(key=lambda entry: entry[4].lower()) # 4 = filename index

			
kPatchConfigFieldNames = ["Name", "Url"]

def GetPatchInstance(filename, desiredName):
	with open(filename, 'r') as file:
		reader = csv.DictReader(file, fieldnames=kPatchConfigFieldNames, dialect='excel-tab')
		reader.next()
			
		for row in reader:
			if row["Name"] == desiredName:
				patch = Patch()
				patch.SetName(row["Name"])
				patch.SetPatchUrl(row["Url"])
				return patch
				
	raise RuntimeError("Failed to find %s!" % (desiredName))
	return None
			
def WriteXmlFile(filename, files):
	file = open(filename, "wb+")
	
	file.write('<ScriptFile>')

	for f in files:
		file.write('\t<CreateLz Input="%s" Output="%s.lz" />\n' % (f, f))

	file.write('</ScriptFile>')
	
def main(argv):
	#
	# Parse command-line arguments
	#
	
	optlist, args = getopt.getopt(argv[1:], 'a:f:p:', ['archive=', 'file=', 'patchcfg='])

	archives = list()
	files = list()
	patchConfigName = None
	
	for name, value in optlist:
		if name == "--archive" or name == "-a":
			files.append(value)
		elif name == "--file" or name == "-f":
			files.append(value)
		elif name == "--patchcfg" or name == "-p":
			patchConfigName = value
			
	#
	# Decide over patch-config to use...
	#
	
	patch = GetPatchInstance("PatchConfig.txt", patchConfigName)
	
	# Add already existing files
	patch.AddFilesFromPatchUrl()
	
	# Process files
	WriteXmlFile("make_patch.xml", files)
	
	os.system("FileArchiver make_patch.xml")

	os.unlink("make_patch.xml")

	# Create patch ZIP
	zip = zipfile.ZipFile("PATCH_%s_%s.zip" % (patchConfigName, date.today().strftime("%m%d%Y")), "w", zipfile.ZIP_DEFLATED)
	
	for file in files:
		patch.AddFile(file)
		file = file + ".lz"
		zip.write(file)
		os.unlink(file)
		
	zip.writestr("crclist", patch.GetCrcList())
	
	zip.close()
	
	#os.system("upload_test " + "PATCH_%s_%s.zip" % (patchConfigName, date.today().strftime("%m%d%Y")))
	#os.remove("PATCH_%s_%s.zip" % (patchConfigName, date.today().strftime("%m%d%Y")))
	
main(sys.argv)