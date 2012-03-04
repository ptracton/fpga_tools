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
import platform
import sim_tool

class modelsim(sim_tool.sim_tool):
    '''
    This is the class that is design to handle Altera Modelsim based verilog simulations.
    We do not use VHDL, verilog only.  This class, handles all directory and file creation
    needed to run a Modelsim simulation.  It will then run the simulation.
    '''


    ################################################################################
    def __init__(self, options, config, args):
        '''
        This is the constructor for the class.  It is the only function needed to be used.
        When the class is instantiated, it will call all the needed functions to set up and
        run the sim.
        '''

        sim_tool.sim_tool.__init__(self, options, config, args)

        ## this is the name of the directory to run the test
        self.sim_dir = self.test_name+"_modelsim_"+self.fpga_type

        return


    ################################################################################
    def generate_sim_files(self):
        '''
        This function will generate the self.sim_file_list contents.  These contents are then fed
        to the simulation tool to run the sim
        '''
        print "\nMODELSIM Generate SIM Files"

        ## update the root since we are going to CD one more level down
        root = self.cfg.root+"../"

        ## attempt to make the directory to run the simulation.  if we fail to make it for
        ## whatever reason, we terminate the sim right here
        try:
            os.mkdir(self.sim_dir)
        except:
            print "Failed to make " + self.sim_dir
            sys.exit(1)

        ## copy the test verilog file to the test run directory and rename it stimulus.v
        ## we rename the file because our testbench includes stimulus.v this will allow us
        ## to make a lot of different tests and not have to modify the testbench to run each one
        command = "cp " +self.test_path+self.test_name+".v "+self.sim_dir+"/stimulus.v"
        os.system(command)

        ## open for WRITING the sim_file_list
        f = open(self.sim_dir+"/"+self.sim_file_list, "w")        

        f.write("vlib work\n\n")

        library = ""

        include_string = ""
        for i in self.cfg.list_include_dirs:
            include_string += "+incdir+"+root+str(i).strip("['],")+" "
        print include_string

        switch_string = ""
        for i in self.switch:
            switch_string += " +define+"+str(i).strip("[']") 

        ## If we are running a XILINX simulation, handle the xilinx specific details
        if self.opts.xilinx:

            ## append a switch so the sim has a define for XILINX
            self.switch.append("XILINX")

            xilinx = os.getenv("XILINX")
            glbl_v = xilinx+"/verilog/src/glbl.v"
            f.write("vlog "+glbl_v + " " + include_string+" " + switch_string + " \n")
            self.cfg.testbench += " work.glbl"
            unisims = xilinx + "/verilog/src/unisims/"
            simprims = xilinx + "/verilog/src/simprims/"
            xilinxcorelib = xilinx + "/verilog/src/XilinxCoreLib/"
            include_string += "+libext+.v -y "+unisims + " -y " + simprims +" -y " +xilinxcorelib
            for i in self.cfg.xilinx.simulation_files:
                f.write("vlog "+ i + " " + include_string+" " + switch_string + " \n")
            for i in self.cfg.xilinx.synthesis_files:
                f.write("vlog "+ root+i.strip("'") + " " + include_string+" " + switch_string + " \n")                

        ## If we are running an ASIC (generic RTL) simulation
        if self.opts.asic:

            ## add a define for ASIC so the sims knows what it is running
            self.switch.append("ASIC")
            
            ## write out the ASIC specific include, simulation and synthesis files
            for i in self.cfg.asic.simulation_files:
                f.write("vlog "+root+i.strip("'") + " " + include_string+" " + switch_string + " \n")

            for i in self.cfg.asic.synthesis_files:
                f.write("vlog "+root+i.strip("'") + " " + include_string+" " + switch_string + " \n")
           

        ## If we are running an Altera simulation in a Xilinx tool....... what were we thinking?!?!?
        ## We were thinking that this should be possible, and it is!
        if self.opts.altera:
            ## add a define for ALTERA so the sims knows what it is running
            self.switch.append("ALTERA")

            ## Need to have altera's modelsim installed so we can grab some files from it
            ## Need to have an environment variable that points to the install so we can find them
            modelsim = os.getenv("MODELSIM")

            ##
            ## Get the path to the altera install so we can get MF libraries
            ##
            altera = os.getenv("ALTERA")

            ##
            ## Always print out the sim files for the simulaiton
            ##
            for i in self.cfg.altera.simulation_files:
                f.write("vlog "+root+i.strip("'") + " " + include_string+" " + switch_string + " \n")

            ##
            ## For RTL sims list all the verilog RTL code
            ##
            for i in self.cfg.altera.synthesis_files:
                f.write("vlog "+root+i.strip("'") + " " + include_string+" " + switch_string + " \n")

            if platform.system() == 'Linux':
                f.write("vlog "+altera+ "/eda/sim_lib/altera_mf.v " + include_string+" " + switch_string + " \n")
            else:
                library = " -L altera_mf_ver "
                
        for i in self.cfg.list_simulation_files:
            f.write("vlog "+root+i.strip("'") + " " + include_string+" " + switch_string + " \n")

        for i in self.cfg.list_synthesis_files:
            f.write("vlog "+root+i.strip("'") + " " + include_string+" " + switch_string + " \n")

        f.write("vsim -voptargs=+acc work."+self.cfg.testbench+" " +switch_string+ " " +library+" \n")

        gui = self.test_path+"/"+self.test_name+".do"
        if self.opts.gui:
            print "GUI" + gui
            if os.path.exists(gui):
                print "USING: " + gui
                f.write("do ../"+gui+"\n")
            else:
                print gui + " does not exist"
        
        f.write("run -all\n\n")        
        f.close()        

        return

    
    ################################################################################
    def run_simulation(self):
        '''
        '''
        print "\nMODELSIM Run Simulation"

        ## switch into the simulation directory, this is why we added another layer to the root variable
        os.chdir(self.sim_dir)
        
        ##
        ## Get the machine type, 64 and 32 bit machine use different libraries
        ##
        stdout_handle = os.popen("uname -m", "r")
        machine =  stdout_handle.read().rstrip('\n')
        if machine == "x86_64":
            lin = "lin64"
        else:
            lin = "lin"

        vlog = self.get_executable("vlog")
        vsim = self.get_executable("vsim")
        vlib = self.get_executable("vlib")
        print "PATH: " + vlog
        print "PATH: " + vsim
        print "PATH: " + vlib

        switch_string = ""
        for i in self.switch:
            switch_string += " +define+"+str(i).strip("[']")         
        print "MODELSIM SWITCHES: " + switch_string

        if os.path.exists("work"):
            os.removedir("work")        

        command = vsim
        if not self.opts.gui:
            command += " -c "
            
        command += " -do simulation_file_list -l "+self.sim_log

            
        os.system(command)

           
        ## go back up to the level we started at
        os.chdir("..")

        
        return
    

    
