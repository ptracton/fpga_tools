#! /usr/bin/env python

import sys
import os

##
## This is the entry point of the program.  Since this is the top program, we do not define classes in this file.
## We instantiate them and use them
##
if __name__ == '__main__':

    argc = len(sys.argv)

    if argc != 2:
        print "You must specify a project!"
        sys.exit(1)

    oc_project = sys.argv[1]
    print "Getting " + oc_project +" from Opencores SVN "
     
    try:
        os.mkdir(oc_project)
    except:
        print "Directory %s already exists" % oc_project
        sys.exit(1)

    os.chdir(oc_project)
    command = "svn co http://opencores.org/ocsvn/"+oc_project+"/"+oc_project+"/trunk"
    print command
    os.system(command)
    os.chdir("..")
        
