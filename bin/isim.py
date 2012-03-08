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

class isim(sim_tool.sim_tool):
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
        self.sim_dir = self.test_name+"_isim_"+self.fpga_type

        return


    ################################################################################
    def generate_sim_files(self):
        '''
        This function will generate the self.sim_file_list contents.  These contents are then fed
        to the simulation tool to run the sim
        '''
        print "\nISIM Generate SIM Files"

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

        ## figure out the include string
        include = ""
        for i in self.cfg.list_include_dirs:
            include += " -i " + root+i.strip("'")

        ## If we are running a XILINX simulation, handle the xilinx specific details
        if self.opts.xilinx:

            ## append a switch so the sim has a define for XILINX
            self.switch.append("XILINX")

            ## get the environment variable that points to where XILINX is installed, we need
            ## this so we can include certain files and libraries in the installation
            xilinx = os.getenv("XILINX")

            ## must simulate the glbl.v file to get xilinx to run correctly
            f.write("verilog work "+xilinx+"/verilog/src/glbl.v \n ")

            ## write out the xilinx specific include, simulation and synthesis files
            for i in self.cfg.xilinx.include_dirs:
                include += " -i " + root+i.strip("'")

            for i in self.cfg.xilinx.synthesis_files:
                f.write("verilog work  "+root+i.strip("'")+" " + include +"\n")
                
            for i in self.cfg.xilinx.simulation_files:
                f.write("verilog work  "+root+i.strip("'")+" " + include +"\n")                

        ## If we are running an ASIC (generic RTL) simulation
        if self.opts.asic:

            ## add a define for ASIC so the sims knows what it is running
            self.switch.append("ASIC")
            
            ## write out the ASIC specific include, simulation and synthesis files
            for i in self.cfg.asic.include_dirs:
                include += " -i " + root+i.strip("'")            
            for i in self.cfg.asic.simulation_files:
                f.write("verilog work  "+root+i.strip("'")+" " + include +"\n")
            for i in self.cfg.asic.synthesis_files:
                f.write("verilog work  "+root+i.strip("'")+" " + include +"\n")

        ## If we are running an Altera simulation in a Xilinx tool....... what were we thinking?!?!?
        ## We were thinking that this should be possible, and it is!
        if self.opts.altera:
            ## add a define for ALTERA so the sims knows what it is running
            self.switch.append("ALTERA")

            ## Need to have altera's modelsim installed so we can grab some files from it
            ## Need to have an environment variable that points to the install so we can find them
            modelsim = os.getenv("MODELSIM")

             ## write out the ALTERA specific include, simulation and synthesis files
            for i in self.cfg.altera.include_dirs:
                include += " -i " + root+i.strip("'")
            for i in self.cfg.altera.simulation_files:
                f.write("verilog work " + root+i.strip("'") +"\n")
            for i in self.cfg.altera.synthesis_files:
                f.write("verilog work " + root+i.strip("'") +"\n")
                
            ## altera_mf (mega function) is a library that we re-compile for isim use, we get this
            ## from the modelsim installation
            f.write("verilog work " + modelsim+ "/altera/verilog/src/altera_mf.v\n")


        ## write out the generic files that work for ASIC/ALTERA/XILINX
        for i in self.cfg.list_simulation_files:
            f.write("verilog work  "+root+i.strip("'")+" " + include +"\n")

        for i in self.cfg.list_synthesis_files:
            f.write("verilog work  "+root+i.strip("'")+" " + include +"\n")

        for i in verilog_files:            
            f.write("verilog work " + i.strip("'")+"\n")
            
        f.close()        

        return

    
    ################################################################################
    def run_simulation(self):
        '''
        '''
        print "\nISIM Run Simulation"

        ## switch into the simulation directory, this is why we added another layer to the root variable
        os.chdir(self.sim_dir)
        print os.getcwd()
        
        ##
        ## Get the machine type, 64 and 32 bit machine use different libraries
        ##
        stdout_handle = os.popen("uname -m", "r")
        machine =  stdout_handle.read().rstrip('\n')
        if machine == "x86_64":
            lin = "lin64"
        else:
            lin = "lin"

        ##
        ## There is a problem with isim and icarus.  They use different and incompatible GLIBC
        ## Make sure isim gets the right one
        ##
        xilinx = os.environ['XILINX']
        xilinx += "/../"
        common = xilinx+"common/lib/"+lin
        ise = xilinx+"ISE/lib/"+lin
        edk = xilinx+"EDK/lib/"+lin
        print xilinx
        os.environ['LD_LIBRARY_PATH'] = common + " " + ise + " " + edk +" " 
        verilog_executable = self.get_executable("fuse")

        self.switch.append("SIMULATION")
        switch_string = ""
        for i in self.switch:
            switch_string += " -d "+str(i).strip("[']") 
        print "ISIM SWITCHES: " + switch_string

        ##
        ## These are a few fields that need updating based on our target.  We can run ALTERA designs in Xilinx ISIM
        ## 
        glbl = ""
        libs = ""
        
        ## For xilixn sims, include the Coregen and Unisim libraries incase they are needed.  If they are not needed
        ## this does not hurt.  Make sure to include work.glbl or the sim will fail to run
        if self.opts.xilinx:
            libs = "-L xilinxcorelib_ver -L unisims_ver "
            glbl = "work.glbl"
            
        ## This runs the fuse command.  In Isim that will generate an .exe file that actually runs the sim
        command = verilog_executable+" " +glbl+ " work."+self.cfg.testbench+" --prj "+self.sim_file_list +" -o "+ self.executable+ " "+ libs+" "+switch_string+" \n"
        print command
        os.system(command)

        ##
        ## If the program exists run it, else we failed to build it so terminate the program
        ##
        if os.path.exists(self.executable):
            if self.opts.gui:
                gui = "-gui -view ../"+self.test_path+"/"+self.test_name+".wcfg"
            else:
                gui = ""

            ## This runs the simulation.....
            command = "./"+self.executable+" -tclbatch ../../src/isim.tcl "+gui+ " -log "+ self.sim_log
            print "EXECUTE: "+ command
            os.system(command)
        else:
            print "Failed to make "+self.executable
            print "Terminate simulation"
            sys.exit(1)
            
        ## go back up to the level we started at
        os.chdir("..")

        ## restore the LD_LIBRARY_PATH so icarus can run next if you want it to
        os.environ['LD_LIBRARY_PATH'] = ""
        
        return
    

    
