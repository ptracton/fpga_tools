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
import pwd
import test_case
import datetime    
import platform

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
    ## 
    ##
    parser.add_option("-t", "--tests", action="store", dest="test_list", help="List of tests to run",)


    ##
    ## Configuration file and root path in relation to where the simulations run from
    ##
    parser.add_option("-r", "--root",     dest="root",     action='store', default="../../", help="The root path")

    ##
    ## Technologies: Altera, Xilinx or "ASIC" which is just generic verilog RTL and not tech specific
    ## You can use as many as you want
    ##
    parser.add_option("-a", "--altera", dest="altera", default=False, action='store_true', help="simulate using Altera defines")
    parser.add_option("-x", "--xilinx", dest="xilinx", default=False, action='store_true', help="simulate using Xilinx defines")
    parser.add_option("-s", "--asic",   dest="asic",   default=False, action='store_true', help="simulate using ASIC defines")

    ##
    ## Simulation Tools:  You can select as many as you want.  With the exception of NCVerilog all of the other tools
    ## are free and easy to get
    ##
    parser.add_option("-m", "--modelsim",  dest="modelsim",  action='store_true', default=False, help="simulate using Altera Modelsim")
    parser.add_option("-i", "--isim",      dest="isim",      action='store_true', default=False, help="simulate using Xilinx Isim")
    parser.add_option("-v", "--verilog",   dest="icarus",    action='store_true', default=False, help="simulate using Icarus Verilog")
    parser.add_option("-c", "--cver",      dest="cver",      action='store_true', default=False, help="simulate using GPL cver")
    parser.add_option("-n", "--ncverilog", dest="ncverilog", action='store_true', default=False, help="simulate using Cadence NC-Verilog")

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
    ## Must choose at least 1 tool to use for regression
    ## 
    if not opts.modelsim and not opts.isim and not opts.icarus and not opts.cver and not opts.ncverilog:
        print "Must choose at least 1 tool, Modelsim, ISIM, Icarus, CVER or NCVerilog"
        sys.exit(1)        

    ##
    ## Create a list of tools to use for the various sims.  
    ##
    tools_list = []
    tools = {}
    if opts.modelsim:
        tools_list.append("-m")
        tools["-m"] = "modelsim"
    if opts.isim:
        tools_list.append("-i")
        tools["-i"] = "isim"
    if opts.icarus:
        tools_list.append("-v")
        tools["-v"] = "icarus"
    if opts.cver:
        tools_list.append("-c")
        tools["-c"] = "cver"
    if opts.ncverilog:
        tools_list.append("-n")
        tools["-n"] = "ncverilog"

    ##
    ## if no technology is specified, let's assume you meant to specify them all
    ## 
    if not opts.asic and not opts.xilinx and not opts.altera:
        print "Must choose at least 1 technology, ASIC, Xilinx or Altera"
        sys.exit(1)
        
    ##
    ## Create the list of which technology switches you plan to use
    ##
    technology_list = []
    technology = {}
    if opts.asic:
        technology_list.append("-s")
        technology["-s"] = "asic"
    if opts.xilinx:
        technology_list.append("-x")
        technology["-x"] = "xilinx"
    if opts.altera:
        technology_list.append("-a")
        technology["-a"] = "altera"        

    ##
    ## If there are no test specified, create a test list from all the .v files in the tests directory
    ##
    test_list = []
    test_dir = opts.root+"tests/"
    if opts.test_list == None:
        print "No test list specified just run all of them"
        file_list = os.listdir(test_dir)
        for i in file_list:
            fname, fext = os.path.splitext(i)
            if fext ==".v":
                test_list.append(fname)
    else:
        test_file = test_dir+opts.test_list
        if not os.path.exists(test_file):
            print "Test List File is missing ",test_file
            sys.exit(1)
        else:
            print "Found file", test_file
            f = open(test_file)
            lines = f.readlines()
            f.close()
            file_list = os.listdir(test_dir)
            for i in file_list:
                for j in lines:
                    if i == j.rstrip():
                        fname, fext = os.path.splitext(i)
                        if fext ==".v":
                            test_list.append(fname)

        
    ##
    ## For each test run it against each of the different simulation tools that are specified
    ##
    test_cases = []
    executable = "run_sim.py"
    for i in test_list:
        for tool in tools_list:
            for tech in technology_list:
                new_test = test_case.test_case(test_name=i, tool=tools[tool], tech=technology[tech])
                test_cases.append(new_test)
                del new_test
                

    reg_log = open('regression_log.txt', 'w')
    now = datetime.datetime.now()
    reg_log.write("USER: %s\n" % pwd.getpwuid( os.getuid() )[ 0 ])
    reg_log.write("PLATFORM: %s \n" % platform.platform())   
    reg_log.write("Regression Start: %s \n\n" % now.strftime("%Y-%m-%d %H:%M:%S"))

    tests_pass = 0
    tests_fail = 0
    tests_total = len(test_cases)
    
    for i in test_cases:
        reg_log.write("\nTEST: " + i.sim_dir)
        i.run()
        if i.status():
            reg_log.write("\tPASSED")
            tests_pass = tests_pass + 1
        else:
            reg_log.write("\tFAILED")
            tests_fail = tests_fail + 1

    percent_pass = (float(tests_pass) / float(tests_total)) * 100
    percent_fail = (float(tests_fail) / float(tests_total)) * 100
    
    reg_log.write("\n\nTOTAL TESTS: %d\n" % tests_total)
    reg_log.write("TOTAL PASS: %d %f\n" % (tests_pass, percent_pass))
    reg_log.write("TOTAL FAIL: %d %f\n" % (tests_fail, percent_fail))
    now = datetime.datetime.now()
    reg_log.write("\n\nRegression Finish: %s \n" % now.strftime("%Y-%m-%d %H:%M:%S"))
    reg_log.close()
    
    ##
    ## All done, terminate program
    ##
    print "\n\nRegression All Done!\n"    
    sys.exit(0)
