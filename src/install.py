#!/usr/bin/python

import shutil, os, glob, stat, time, sys
import distutils.cmd, distutils.sysconfig


destination_posix = "/opt/galleryforge"
destination_nt = "c:\\galleryforge"

symlinks = "/opt/bin"
if os.name == "nt":
	shortcuts = os.environ["USERPROFILE"]

dirs = "bin", "demo", "doc", "galleryforge"


def sed(filename, search, replace):
	file = open(filename, 'r')
	nfile = open(filename + ".sed", 'w')
	for line in file.xreadlines():
		line = line.replace(search, replace)
		nfile.write(line)
	file.close()
	nfile.close()
	os.remove(filename)
	os.rename(filename+".sed", filename)


def getRXChmod():
	return stat.S_IRWXU+stat.S_IRGRP+stat.S_IXGRP+stat.S_IROTH+stat.S_IXOTH


def osNT():
	if os.name == "nt":
		return True
	return False


def getPython():
	if osNT():
		return os.path.join(distutils.sysconfig.PREFIX, "python.exe")
	else:
		return os.path.join(distutils.sysconfig.PREFIX, "bin", "python")


def install():
	sympath = symlinks
	destination = destination_posix
	puredest = None
	if osNT():
		destination = destination_nt
		puredest = destination_nt
	else:
		destination = destination_posix
		puredest = destination_posix
		if len(sys.argv) > 1:
			destination = os.path.join(sys.argv[1], destination_posix[1:])
			sympath = os.path.join(sys.argv[1], symlinks[1:])

	# distribute
	for d in dirs:
		if not os.path.exists(destination):
			os.makedirs(destination)
		if os.path.exists(os.path.join(destination, d)):
			shutil.rmtree(os.path.join(destination, d))
		shutil.copytree(d, os.path.join(destination, d))
	
	# fix executables
	for i in glob.glob(os.path.join(destination, "bin") + os.sep + "*"):
		sed(i, "#!/usr/bin/python", "#!"+getPython())
		sed(i, "None", os.path.join(puredest, "galleryforge"))
		os.chmod(i, getRXChmod())
		
		# create shortcuts
		pyfile = os.path.split(i)[1]
		exefile = os.path.split(i)[1].split(".")[0]
		if osNT():
			if i.find("gui") != -1:
				shutil.copyfile(i, os.path.join(shortcuts, "Desktop", pyfile))
#			distutils.cmd.create_shortcut(
#				os.path.join(shortcuts, "Desktop", pyfile),
#				"", os.path.join(destination, "bin", pyfile))
		else:
			if not os.path.exists(sympath):
				os.makedirs(sympath)
			if os.path.lexists(os.path.join(sympath, exefile)):
				os.remove(os.path.join(sympath, exefile))
 			os.symlink(os.path.join(destination, "bin", pyfile),
 				os.path.join(sympath, exefile))
	
	if os.name == "nt":
		print "Install successful"
		time.sleep(3)



if __name__ == "__main__":
	install()
