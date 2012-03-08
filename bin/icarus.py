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

class icarus(sim_tool.sim_tool):
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
        self.sim_dir = self.test_name+"_icarus_"+self.fpga_type

        return
    
    ################################################################################
    def generate_sim_files(self):
        '''
        This function will generate the self.sim_file_list contents.  These contents are then fed
        to the simulation tool to run the sim
        '''
        print "\nICARUS Generate SIM Files"

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
        
        if self.opts.xilinx:
            print "ICARUS XILINX\n"
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
            print "ICARUS ALTERA\n"
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

        for i in self.cfg.list_include_dirs:
            f.write("+incdir+"+root+i+"\n")

        for i in self.cfg.list_simulation_files:
            f.write(root+i.strip("'")+"\n")

        for i in self.cfg.list_synthesis_files:
            f.write(root+i.strip("'")+"\n")

        for i in verilog_files:
            f.write(i.strip("'")+"\n")

        f.close()        

        return

  ################################################################################
    def run_simulation(self):
        '''
        '''
        print "\nISIM Run Simulation"

        ## switch into the simulation directory, this is why we added another layer to the root variable
        os.chdir(self.sim_dir)

        ##
        ## Find the executable we need to run this simulation
        ##
        verilog_executable = self.get_executable("iverilog")

        ##
        ## Get our list of switches turned into a string for use 
        ##
        switch_string = ""
        for i in self.switch:
            switch_string += " -D"+str(i).strip("[']")        
        print "ICARUS SWITCHES: " + switch_string

        ##
        ## Create the executable for the simulation, icarus generates a program to run as the simulation
        ##
        command = verilog_executable + " -Wtimescale "+ switch_string  +" -o " + self.executable + " -f " + self.sim_file_list
        print "Icarus Command: " + command
        os.system(command)

        ##
        ## If the program exists run it, else we failed to build it so termiante the program
        ##
        if os.path.exists(self.executable):
            os.system("vvp -l "+self.sim_log +" ./"+self.executable)
        else:
            print "Failed to make "+self.executable
            print "Terminate simulation"
            sys.exit(1)


        ##
        ## If --gui is specified, start GKTWAVE with the dump file and any wave file with the right name
        ## in the right location
        ##
        if self.opts.gui:
            print "RUNNING GUI GTKWAVE"
            gui_wave = self.cfg.root+"/tests/"+self.test_name+".wav.sav"
            if not os.path.exists(gui_wave):
                print gui_wave + " FILE NOT FOUND"
                gui_wave = ""
                
            print "WAVE FILE: " + gui_wave
                       
            gui_executable = self.get_executable("gtkwave")
            command = gui_executable +" dump.vcd " + gui_wave
            print command
            os.system(command)            

        ## go back up to the level we started at
        os.chdir("..")

        ## restore the LD_LIBRARY_PATH so icarus can run next if you want it to
        os.environ['LD_LIBRARY_PATH'] = ""
        
        return            
