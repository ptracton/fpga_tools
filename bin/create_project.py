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

def soc_project(project_name):

    print "\n\nCreating SOC Project: " + project_name

    ##
    ## DIR STRUCTURE:  project_name
    ##                    cores
    ##                    document
    ##                    fpga


    if (os.path.exists(project_name)):
        print "Project: "+project_name+" already exists"
        sys.exit(1)

    project_dirs = []
    project_dirs.append(project_name+"/cores")
    project_dirs.append(project_name+"/document")
    project_dirs.append(project_name+"/fpga")

  
    list_to_dirs(project_dirs)
    
    return

def fpga_project(project_name):

    print "\n\nCreating FPGA Project: " + project_name

    ##
    ## DIR STRUCTURE:  project_name
    ##                 bench 
    ##                    behavioral
    ##                    includes
    ##                 configurations
    ##                 document
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
    ##                  software
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
    project_dirs.append(project_name+"/bench/verilog/tasks")
    project_dirs.append(project_name+"/configurations")
    project_dirs.append(project_name+"/document")
    project_dirs.append(project_name+"/rtl/verilog/"+project_name)
    project_dirs.append(project_name+"/sim/ppr_sim/bin")
    project_dirs.append(project_name+"/sim/ppr_sim/run")
    project_dirs.append(project_name+"/sim/ppr_sim/src")
    project_dirs.append(project_name+"/sim/rtl_sim/bin")
    project_dirs.append(project_name+"/sim/rtl_sim/run")
    project_dirs.append(project_name+"/sim/rtl_sim/src")
    project_dirs.append(project_name+"/sim/tests")
    project_dirs.append(project_name+"/synthesis/")
    project_dirs.append(project_name+"/software/RTOS")
    project_dirs.append(project_name+"/software/applications")
    
    list_to_dirs(project_dirs)

    
    return

def core_project(project_name):

    print "\n\nCreating Core Project: " + project_name

    ## Name
    ##   document
    ##   drivers
    ##     devices
    ##        cpu (several options, lm8, lm32, etc...)
    ##          devices
    ##          services
    ##     services
    ##   rtl
    ##     verilog
    ##   sim
    ##      tests
    ##      run
    ##  bench
    ##      verilog

    if (os.path.exists(project_name)):
        print "Project: "+project_name+" already exists"
        sys.exit(1)

    project_dirs = []
    project_dirs.append(project_name+"/document")
    project_dirs.append(project_name+"/drivers")
    project_dirs.append(project_name+"/drivers/lm8")
    project_dirs.append(project_name+"/drivers/lm8/devices")
    project_dirs.append(project_name+"/drivers/lm8/services")
    project_dirs.append(project_name+"/drivers/lm32")
    project_dirs.append(project_name+"/drivers/lm32/devices")
    project_dirs.append(project_name+"/drivers/lm32/services")
    project_dirs.append(project_name+"/drivers/or1200")
    project_dirs.append(project_name+"/drivers/or1200/devices")
    project_dirs.append(project_name+"/drivers/or1200/services")
    project_dirs.append(project_name+"/drivers/aemb")
    project_dirs.append(project_name+"/drivers/aemb/devices")
    project_dirs.append(project_name+"/drivers/aemb/services")
    project_dirs.append(project_name+"/sim/rtl_sim/bin")
    project_dirs.append(project_name+"/sim/rtl_sim/run")
    project_dirs.append(project_name+"/sim/rtl_sim/src")
    project_dirs.append(project_name+"/sim/tests")    
    project_dirs.append(project_name+"/rtl")
    project_dirs.append(project_name+"/rtl/verilog/")
    project_dirs.append(project_name+"/bench/verilog/includes")
    project_dirs.append(project_name+"/bench/verilog/tasks")
    project_dirs.append(project_name+"/configurations")
    
    list_to_dirs(project_dirs)
    
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
    parser.add_option("-d", "--debug",   dest="debug",  action='store_true', help="turns on debugging print statements")
    parser.add_option(      "--soc",     dest="soc",    action='store_true', help="Create a System On Chip project")
    parser.add_option(      "--fpga",    dest="fpga",   action='store_true', help="Create an FPGA Project")
    parser.add_option(      "--core",    dest="core",   action='store_true', help="Create a core project")
   

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

    project_count = 0
    if (opts.soc):
        project_count = project_count + 1
    if (opts.fpga):
        project_count = project_count + 1
    if (opts.core):
        project_count = project_count + 1

    if (project_count != 1):
        print "Multiple project types set! Choose only 1 of soc, fpga or core"
        sys.exit(1)

    project_name = str(args[0]).strip("[']")

    if (opts.soc):
        soc_project(project_name)
    if (opts.fpga):
        fpga_project(project_name)
    if (opts.core):
        core_project(project_name)


    ##
    ## All done, terminate program
    ##
    print "\n\nAll Done!\n"    
    sys.exit(0)
