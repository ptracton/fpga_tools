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

import sys
import os
import config_file
import glob

class sim_tool:
    '''
    This is the base class for any simulation tool.  Here we keep all the common things
    that a simulation will perform.
    '''

    ################################################################################
    def __init__(self, options, config, args):

        ## opts are the command line options
        self.opts = options

        ## cfg is the config file object
        self.cfg = config

        ## test_name is the name of this test case that we are running
        self.test_name = str(args[0]).strip("[']")

        ## executable is needed since fuse (xilinx sim tool) creates an executable to run the
        ## simulation.  icarus does the same thing, modelsim and ncverilog do NOT
        self.executable = self.test_name+".exe"

        ## Log file from running the sim
        self.sim_log = self.test_name+".log"

        ## switches or options for this test run
        self.switch = []

        ## by checking the options we can create a string for which type of simulation we are running
        self.fpga_type = "xilinx"        
        if options.xilinx:
            self.fpga_type = "xilinx"
        if options.altera:
            self.fpga_type = "altera"
        if options.asic:
            self.fpga_type = "asic"

        ## This is the file in the directory that tells the simulation how to run
        self.sim_file_list ="simulation_file_list"

        ## This is the path to the test cases 
        self.test_path="../../tests/"            

        ## Keep track of building the FW
        self.built_firmware = False
        
        return

    ################################################################################
    def get_executable(self, executable):
        '''
        Utility function to get the absolute path for an executable.
        This is used by all simulations to find the actual program
        that simulates the design
        '''
        stdout_handle = os.popen("which "+executable, "r")
        return stdout_handle.read().rstrip('\n') 


    ################################################################################
    def clean_sim(self):
        '''
        Remove the directory with the results from the last time we ran this simulation
        '''
        print "Cleaning Sim " + self.sim_dir

        command = "rm -rf " + self.sim_dir
        print command

        ## try to remove the old directory, if it is not there, os.system throws an exception
        ## so we catch it and move on
        try:
            os.system("rm -rf " + self.sim_dir)
        except:
            print self.sim_dir+" is already gone!"

    ################################################################################
    def generate_sim_files(self):
        print "OVER RIDE THIS FUNCTION!"
        return
    
    ################################################################################
    def run_simulation(self):
        print "OVER RIDE THIS FUNCTION!"
        return

    ################################################################################
    def simulation_complete(self):
        complete = self.sim_dir+"/simulation_complete"
        command = "touch " + complete
        os.system(command)
        return

    ################################################################################
    def find_verilog_files(self, path):
        verilog_files = []
        os.chdir(path)
        for files in glob.glob("*.v"):
            if (files != "stimulus.v"):
                print os.getcwd()+"/"+files
                verilog_files.append(os.getcwd()+"/"+files)

        os.chdir("..")
        return verilog_files

    ################################################################################
    def build_firmware(self):
        print "Building Firmware"
        
        if (os.path.exists("../src/Makefile")):
            print "Found Makefile, build firmware"
            make_options = "TEST_NAME="+self.test_name+" TECHNOLOGY="+self.fpga_type


            simulator = ""
            if (self.opts.modelsim):
                simulator = "modelsim"
            else:
                if (self.opts.isim):
                    simulator = "isim"
                else:
                    if (self.opts.icarus):
                        simulator = "icarus"                
                    else:
                        if (self.opts.cver):
                            simulator = "cver"
                        else:
                            if (self.opts.ncverilog):
                                simulator = "ncverilog"                
                
            make_options += " SIMULATOR="+simulator

            command = "make -f ../src/Makefile "+make_options
            print command
            os.system(command)
            
            self.built_firmware = True
        else:
            print "No Firmware to build"
            self.built_firmware = False
            
        return
