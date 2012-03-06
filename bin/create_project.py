#! /usr/bin/env python

################################################################################
#
# $Header:$
# $Revision:$
# $State:$
# $Date:$
# $Author:$
#
# Original Author: Phil Tracton ptracton@gmail.com
#
# Description: 
#
# $Log:$
#
################################################################################

import optparse
import sys
import os
import shutil

def install_files(src, dst):
    shutil.copy2(src+"/skeleton/fpga.cfg", dst+"/configurations/")
    shutil.copy2(src+"/skeleton/testbench.v", dst+"/bench/verilog/")
    shutil.copy2(src+"/skeleton/dump.v", dst+"/bench/verilog/")
    shutil.copy2(src+"/skeleton/timescale.v", dst+"/bench/verilog/includes")
    return

def safe_mkdir(path):
    try:
        os.makedirs(path)
    except:
        print "Failed to make " + path
        sys.exit(1)
    return

def list_to_dirs(dirs):
    
    for i in dirs:
        print i.strip("[']")
        safe_mkdir(i.strip("[']"))
    return

##
## This is the entry point of the program.  Since this is the top program, we do not define classes in this file.
## We instantiate them and use them
##
if __name__ == '__main__':

    ##
    ## Read the command line options
    ##
    parser = optparse.OptionParser()

    ##
    ## Support switches.  They handle various tasks
    ##
    parser.add_option("-d", "--debug",   dest="debug",   action='store_true', help="turns on debugging print statements")
   

    ##
    ## Get the options dictionary and list of arguments passed in from CLI
    ##
    (opts, args) = parser.parse_args()

    ##
    ## Display the options passed in if you use the -d switch
    ##
    if opts.debug:
        print opts
        print args

    ##
    ## Make sure the user specified a test case to run otherwise there is no stimulus file to copy
    ## and the test will fail to run
    ##
    if not args:
        print "Must specify a project name!"
        sys.exit(1)

    project_name = str(args[0]).strip("[']")
    print "\n\nCreating Project: " + project_name


    ##
    ## DIR STRUCTURE:  project_name
    ##                 bench 
    ##                    behavioral
    ##                    includes
    ##                 configurations
    ##                 docs
    ##                 rtl
    ##                    verilog
    ##                       project_name (top level instance)
    ##                 sim
    ##                    ppr_sim
    ##                       bin
    ##                       run
    ##                       src
    ##                     rtl_sim
    ##                        bin
    ##                        run
    ##                        src
    ##                     tests
    ##                 synthesis
    ##                     xilinx
    ##                     altera
    ##                     asic
    ##                  software
    ##                     drivers
    ##                        src
    ##                        includes
    ##                        objects
    ##                        library
    ##                     RTOS
    ##                     application
    ##
    ##

    if (os.path.exists(project_name)):
        print "Project: "+project_name+" already exists"
        sys.exit(1)

    project_dirs = []
    project_dirs.append(project_name+"/bench/verilog/behavioral")
    project_dirs.append(project_name+"/bench/verilog/includes")
    project_dirs.append(project_name+"/configurations")
    project_dirs.append(project_name+"/docs")
    project_dirs.append(project_name+"/rtl/verilog/"+project_name)
    project_dirs.append(project_name+"/sim/ppr_sim/bin")
    project_dirs.append(project_name+"/sim/ppr_sim/run")
    project_dirs.append(project_name+"/sim/ppr_sim/src")
    project_dirs.append(project_name+"/sim/rtl_sim/bin")
    project_dirs.append(project_name+"/sim/rtl_sim/run")
    project_dirs.append(project_name+"/sim/rtl_sim/src")
    project_dirs.append(project_name+"/sim/tests")
    project_dirs.append(project_name+"/synthesis/asic")
    project_dirs.append(project_name+"/synthesis/xilinx")
    project_dirs.append(project_name+"/synthesis/altera")
    project_dirs.append(project_name+"/software/drivers/src")
    project_dirs.append(project_name+"/software/drivers/includes")
    project_dirs.append(project_name+"/software/drivers/objects")
    project_dirs.append(project_name+"/software/drivers/library")
    project_dirs.append(project_name+"/software/RTOS")
    project_dirs.append(project_name+"/software/drivers/applications")
    
    list_to_dirs(project_dirs)

    executable = os.path.abspath(__file__ )
    [path, script_name] = os.path.split(executable)
    
    install_files(str(path), project_name)

    ##
    ## All done, terminate program
    ##
    print "\n\nAll Done!\n"    
    sys.exit(0)
