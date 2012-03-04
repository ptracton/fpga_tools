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
import config_file
import isim
import modelsim
import icarus
import cver

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
    ## Configuration file and root path in relation to where the simulations run from
    ##
    parser.add_option("-r", "--root",     dest="root",     action='store', default="../../../", help="The root path")
    parser.add_option("-f", "--cfg_file", dest="cfg_file", action='store', default="fpga.cfg",     help="The configuration file to use")

    ##
    ## Technologies: Altera, Xilinx or "ASIC" which is just generic verilog RTL and not tech specific
    ## You can only use 1 of these at a time.  Each one will set a define for the simulation, ALTERA, XILINX or ASIC
    ##
    parser.add_option("-a", "--altera", dest="altera", action='store_true', help="simulate using Altera defines")
    parser.add_option("-x", "--xilinx", dest="xilinx", action='store_true', help="simulate using Xilinx defines")
    parser.add_option("-s", "--asic",   dest="asic",   action='store_true', help="simulate using ASIC defines")

    ##
    ## Simulation Tools:  You can select only 1 at a time to run.  With the exception of NCVerilog all of the other tools
    ## are free and easy to get
    ##
    parser.add_option("-m", "--modelsim",  dest="modelsim", action='store_true', help="simulate using Altera Modelsim")
    parser.add_option("-i", "--isim",      dest="isim",     action='store_true', help="simulate using Xilinx Isim")
    parser.add_option("-v", "--verilog",   dest="icarus",   action='store_true', help="simulate using Icarus Verilog")
    parser.add_option("-c", "--cver",      dest="cver",     action='store_true', help="simulate using GPL cver")
    parser.add_option("-n", "--ncverilog", dest="ncverilog", action='store_true', help="simulate using Cadence NC-Verilog")

    ##
    ## Timing simulation or RTL?  RTL is the default, but if you use this option we will run timing sims
    ##
    parser.add_option("-t", "--timing", dest="timing", action='store_true', help="run a timing or post place and route sim")

    ##
    ## Support switches.  They handle various tasks
    ##
    parser.add_option("-g", "--gui",     dest="gui",     action='store_true', help="automatically start the GUI waveform viewer")    
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
    if args == "":
        print "Must specify a test to run!"
        sys.exit(1)

    ##
    ## Check to make sure only 1 technology is enabled per simulation.  These will resolve into defines in the verilog
    ## code, so turning on more than 1 would scramble things
    ##
    tech_enabled = 0
    
    if opts.altera:
        tech_enabled = tech_enabled +1
        
    if opts.xilinx:
        tech_enabled = tech_enabled +1
        
    if opts.asic:
        tech_enabled = tech_enabled +1

    if tech_enabled != 1:
        print "Selected too many or too few technologies selected, you can only have 1"
        print opts
        sys.exit(1)

    ##
    ## Create a simulation object, fill in the details
    ##
    Cfg = config_file.config_file(opts, file_name=opts.cfg_file, root=opts.root)

    ##
    ## Figure out which type of sim to run and go run it.  Also make sure only
    ## 1 tool is selected
    ##
    if opts.modelsim:
        Sim = modelsim.modelsim(opts, Cfg, args)

    if opts.isim:
        Sim = isim.isim(opts, Cfg, args)

    if opts.icarus:
        Sim = icarus.icarus(opts, Cfg, args)

    if opts.cver:
        Sim = cver.cver(opts, Cfg, args)
        
    if opts.ncverilog:
        print "ncverilog to be done"


    ## Clean up the last run of the sim, do not want a mix of old and new data
    Sim.clean_sim()
    
    ## Create the simulation directory, and put all needed files in it
    Sim.generate_sim_files()
    
    ## Run the simulation
    Sim.run_simulation()
    
    ##
    ## All done, terminate program
    ##
    print "\n\nAll Done!\n"    
    sys.exit(0)
