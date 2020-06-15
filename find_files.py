import os

mypath = "C:\\Users\\Administrator\\Desktop\\rb\\client"
f = open('filelist', 'a')
exclude = ("CRYPTION", ".git", "pylib")
excludeFile = ("find_files.py", "loginInfo.txt", "make_patch.py", "syserr.txt", ".gitignore", "filelist", "find_files.py", "camy_enable", "PatchConfig.txt", ".gitignore", "FileArchiver.exe", "gameoption.cfg", "locale.cfg", "mylang.cfg")
if f:
	for root, directories, filenames in os.walk(mypath, topdown=True):
		directories[:] = [d for d in directories if d not in exclude]
		filenames[:] = [file for file in filenames if file not in excludeFile]
		for filename in filenames: 
			f.write(" -f "+os.path.join(root,filename)+" ") 


print "OVER"