# First off, I have no love for python so don't get all judgy on the un-1337 code please
# 
# This is a hack to quickly triage Android devices for patterns and files and pull the
# for post analysis
# 
# syntax: $ AndroidProcGrab.py
# 
# Basically, call it and get a folder with a full file listing and the [file only] 
#  contents of the /proc/ directory
#  	
#  enjoy and have fun
#  @m0nk_dot	

import subprocess
import sys

fileName = subprocess.check_output(["adb", "devices"]);

#ugly, i know
fileName = fileName.split();
dirName = fileName[4];
dirName = dirName.strip();

print "Making a folder for: " + dirName;

subprocess.call(["mkdir", "-p", dirName + "/proc"]);

print "Generating file listings and pulling down"
subprocess.call(["adb", "shell", "find", ">/sdcard/Download/fullFileList.txt"]);
subprocess.call(["adb", "pull", "/sdcard/Download/fullFileList.txt", dirName + "/"]);

searchFiles = subprocess.check_output([ "adb", "shell",  "ls -la /proc/ | grep \^\-|awk '{print $NF}' " ]);
searchFiles = searchFiles.splitlines();


print 'Number of arguments:', len(searchFiles), 'arguments.'
print 'Argument List:', str(searchFiles)



for line in searchFiles:
 	#print line;
	if line != "kmsg":
		subprocess.call(["adb", "pull", "/proc/" + line, dirName + "/proc/"]);
 		print "pulling: " + dirName + "/proc/" + line;
 	
