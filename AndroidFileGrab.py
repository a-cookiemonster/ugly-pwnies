# First off, I have no love for python so don't get all judgy on the un-1337 code please
# 
# This is a hack to quickly triage Android devices for patterns and files and pull the
# for post analysis
# 
# syntax: $ AndroidFileGrab.py [first string to search for] [second string to search for] [etc]
# 
# Basically, call it with a space seperated list of any string you care about.
# 
# The script will:
#  	1. connect to Android over adb
#  	2. generate a folder based on the device ID
#  	3. dump a full file listing of the device into the root dir it just created
#  	4. scan and download all files or folders matching any of the search words
#  	5. bonus, it rebuilds the folder structure of the device.
#  	
#  enjoy and have fun
#  @m0nk_dot	

import subprocess
import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

fileName = subprocess.check_output(["adb", "devices"]);

#ugly, i know
fileName = fileName.split();
dirName = fileName[4];
dirName = dirName.strip();

print "Making a folder for: " + dirName;

subprocess.call(["mkdir", dirName]);

print "Generating file listings and pulling down"
subprocess.call(["adb", "shell", "find", ">/sdcard/Download/fullFileList.txt"]);
subprocess.call(["adb", "pull", "/sdcard/Download/fullFileList.txt", dirName + "/"]);

searchArgs = sys.argv;
i=1;
while i < len(sys.argv):
	print "\n\nSearching and copying: " + searchArgs[i];
	
	searchTerm = searchArgs[1];
	
	#match files
	searchFiles = subprocess.check_output(["grep", searchTerm, dirName + "/fullFileList.txt"]);	
	searchFiles = searchFiles.splitlines();
	for line in searchFiles:
		print line;
		line = line.lstrip('.');
		dir = line.rpartition('/');
		
		subprocess.call(["mkdir", "-p", dirName + dir[0]]);
		subprocess.call(["adb", "pull", line, dirName + dir[0] + "/"]);
	i = i+1;