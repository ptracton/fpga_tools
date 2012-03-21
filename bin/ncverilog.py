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
import sim_tool

class ncverilog(sim_tool.sim_tool):
    '''
    This is the class that is design to handle Xilinx ISIM based verilog simulations.
    We do not use VHDL, verilog only.  This class, handles all directory and file creation
    needed to run an Isim simulation.  It will then run the simulation.
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
        self.sim_dir = self.test_name+"_ncverilog_"+self.fpga_type

        return
    
    ################################################################################
    def generate_sim_files(self):
        '''
        This function will generate the self.sim_file_list contents.  These contents are then fed
        to the simulation tool to run the sim
        '''
        print "\nNCVERILOG Generate SIM Files"

        ## update the root since we are going to CD one more level down
        root = self.cfg.root+"../"

        ## attempt to make the directory to run the simulation.  if we fail to make it for
        ## whatever reason, we terminate the sim right here
        try:
            os.mkdir(self.sim_dir)
        except:
            print "Failed to make " + self.sim_dir
            sys.exit(1)

        ##
        ## If we are doing some kind of SOC with a CPU and FW, build the firmware
        ##
        self.build_firmware()
        verilog_files = self.find_verilog_files(self.sim_dir)
        print verilog_files

        ## copy the test verilog file to the test run directory and rename it stimulus.v
        ## we rename the file because our testbench includes stimulus.v this will allow us
        ## to make a lot of different tests and not have to modify the testbench to run each one
        command = "cp " +self.test_path+self.test_name+".v "+self.sim_dir+"/stimulus.v"
        os.system(command)

        ## open for WRITING the sim_file_list
        f = open(self.sim_dir+"/"+self.sim_file_list, "w")        

        f.write("+verbose\n");
        f.write("+speedup\n");
        f.write("+libext+.v+\n")

        if self.opts.xilinx:
            print "NCVERILOG XILINX\n"
            f.write("+libext+.v\n")
            xilinx = os.getenv("XILINX")
            f.write("-y " + xilinx + "/verilog/src/unisims/\n")
            f.write("-y " + xilinx + "/verilog/src/simprims/\n")
            f.write("-y " + xilinx + "/verilog/src/XilinxCoreLib/\n")
            f.write(xilinx+"/verilog/src/glbl.v \n ")

            for i in self.cfg.xilinx.include_dirs:
                f.write("+incdir+"+root+i+"\n")
            for i in self.cfg.xilinx.simulation_files:
                f.write(root+i.strip("'") +"\n")
            for i in self.cfg.xilinx.synthesis_files:
                f.write(root+i.strip("'") +"\n")            

        if self.opts.altera:
            print "NCVERILOG ALTERA\n"
            altera = os.getenv("ALTERA")
            modelsim = os.getenv("MODELSIM")

            f.write("-y " + modelsim+ "/altera/verilog/src\n")
            f.write("+incdir+" + modelsim+ "/altera/verilog/src\n")
            f.write(modelsim+ "/altera/verilog/src/altera_mf.v\n")
            
            for i in self.cfg.altera.include_dirs:
                f.write("+incdir+"+root+i+"\n")
            for i in self.cfg.altera.simulation_files:
                f.write(root+i.strip("'") +"\n")
            for i in self.cfg.altera.synthesis_files:
                f.write(root+i.strip("'") +"\n")

        if self.opts.asic:
            for i in self.cfg.asic.include_dirs:
                f.write("+incdir+"+root+i+"\n")

            for i in self.cfg.asic.simulation_files:
                f.write(root+i.strip("'")+"\n")
                    
            for i in self.cfg.asic.synthesis_files:
                f.write(root+i.strip("'")+"\n")

        for i in self.cfg.core_include_dirs:
            f.write("+incdir+"+i.strip("'")+"\n")

        for i in self.cfg.list_include_dirs:
            f.write("+incdir+"+root+i+"\n")

        for i in self.cfg.list_simulation_files:
            f.write(root+i.strip("'")+"\n")

        for i in self.cfg.list_synthesis_files:
            f.write(root+i.strip("'")+"\n")

        for i in verilog_files:
            f.write(i.strip("'")+"\n")
            
        for i in self.cfg.core_simulation_files:
            f.write(i.strip("'")+"\n")

        for i in self.cfg.core_synthesis_files:
            f.write(i.strip("'")+"\n")

        f.close()        

        return

  ################################################################################
    def run_simulation(self):
        '''
        '''
        print "\nNCVERILOG Run Simulation"

        ## switch into the simulation directory, this is why we added another layer to the root variable
        os.chdir(self.sim_dir)

        ##
        ## Find the executable we need to run this simulation
        ##
        verilog_executable = self.get_executable("ncverilog")

        ##
        ## Get our list of switches turned into a string for use 
        ##
        switch_string = ""
        for i in self.switch:
            switch_string += " +define+"+str(i).strip("[']")        
        print "NCVERILOG SWITCHES: " + switch_string

        ##
        ## Create the executable for the simulation, ncverilog generates a program to run as the simulation
        ##
        command = verilog_executable + " "+ switch_string  +" -f " + self.sim_file_list + " -l " + self.sim_log + " +define+NCVERILOG +access+rwc "
        print "NCVerilog Command: " + command
        os.system(command)

        ##
        ## If --gui is specified, start GKTWAVE with the dump file and any wave file with the right name
        ## in the right location
        ##
        if self.opts.gui:
            print "RUNNING GUI Simvision"
            gui_wave = self.cfg.root+"/tests/"+self.test_name+".sv"
            if not os.path.exists(gui_wave):
                print gui_wave + " FILE NOT FOUND"
                gui_wave = ""
                
            print "WAVE FILE: " + gui_wave
                       
            gui_executable = self.get_executable("simvision")
            command = gui_executable +" -input " + gui_wave
            args = " -input " + gui_wave
            print command
#            os.spawnlp(os.P_NOWAIT, gui_executable, args)
            os.system(command)


        ## go back up to the level we started at
        os.chdir("..")

        return            
