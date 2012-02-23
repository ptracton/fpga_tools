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

import os
import sys
import re
import fpga

################################################################################
#
#
#
################################################################################
class config_file:
    '''
    '''

    ############################################################################
    #
    #
    #
    ############################################################################
    def __init__(self, opts, file_name="test.cfg", root="MUST BE SET"):
        '''
        '''
        self.root = root
        self.opts = opts
        self.file_name = file_name
                
        self.list_simulation_files = []
        self.list_synthesis_files = []
        self.list_include_dirs = [] 

        self.project = ""
        self.testbench = ""
        self.testbench_instance = ""
        self.design_top_level = ""

        self.xilinx = fpga.fpga()
        self.altera = fpga.fpga()
        self.asic = fpga.fpga()
        
        self.parse_file()
        
        return

    def __str__(self):
        return "Config File"

    def __help__(self):
        return "Config File"

 
    ############################################################################
    #
    #
    #
    ############################################################################    
    def parse_file(self):
        '''
        '''

        cfg_file = self.root+"configurations/"+self.file_name

        if self.opts.debug:
            print "ROOT: " + self.root
            print "CFG: " + self.file_name
        
        if not os.path.exists(cfg_file):
            print cfg_file + " does NOT exist, terminate program"
            sys.exit(1)
            
        else:
            f = open(cfg_file)
            lines = f.readlines()
            f.close()
            print "Parsing File: ", self.file_name
            
        for i in lines:
            if i[0] != "#":
                project = re.search('PROJECT:(.*)',i)
                if project:
                    self.project = project.group(1).lstrip()                  
                    print "Project = " + self.project

                tb = re.search('TESTBENCH:(.*)', i)
                if tb:
                    print "Test Bench Name ="+tb.group(1).lstrip()
                    self.testbench=tb.group(1).lstrip()

                tb_inst = re.search('TESTBENCH_INSTANCE:(.*)', i)
                if tb_inst:
                    print "Test Bench Instance ="+tb_inst.group(1).lstrip()
                    self.testbench_instance=tb_inst.group(1).lstrip()
                    
                design = re.search('DESIGN_TOP_LEVEL:(.*)', i)
                if design:
                    print "Design Top Level ="+design.group(1).lstrip()
                    self.design_top_level=design.group(1).lstrip()




                include = re.search('^INCLUDE:(.*)', i)
                if include:
                    print "Include = " + include.group(1).lstrip()
                    self.list_include_dirs.append(include.group(1).lstrip())

                synthesis = re.search('^SYNTHESIS:(.*)', i)
                if synthesis:
                    print "Synthesis = " + synthesis.group(1).lstrip()
                    self.list_synthesis_files.append(synthesis.group(1).lstrip())
                    
                simulation = re.search('^SIMULATION:(.*)', i)
                if simulation:
                    print "Simulation = " + simulation.group(1).lstrip()
                    self.list_simulation_files.append(simulation.group(1).lstrip())
                    


                altera_include = re.search('^ALTERA_INCLUDE:(.*)', i)
                if altera_include:
                    print "Altera Include Dirs = " + altera_include.group(1).lstrip()
                    self.altera.include_dirs.append(altera_include.group(1).lstrip())

                altera_simulation = re.search('^ALTERA_SIMULATION:(.*)', i)
                if altera_simulation:
                    print "Altera Simulation = " + altera_simulation.group(1).lstrip()
                    self.altera.simulation_files.append(altera_simulation.group(1).lstrip())

                altera_fpga = re.search('^ALTERA_FPGA:(.*)', i)
                if altera_fpga:
                    print "Altera Fpga = " + altera_fpga.group(1).lstrip()
                    self.altera.fpga_model = altera_fpga.group(1).lstrip()

                altera_netlist = re.search('^ALTERA_NETLIST:(.*)', i)
                if altera_netlist:
                    print "Altera Netlist = " + altera_netlist.group(1).lstrip()
                    self.altera.netlist = altera_netlist.group(1).lstrip()

                altera_sdf = re.search('^ALTERA_SDF:(.*)', i)
                if altera_sdf:
                    print "Altera SDF = " + altera_sdf.group(1).lstrip()
                    self.altera.sdf = altera_sdf.group(1).lstrip()

                altera_constraints = re.search('^ALTERA_CONSTRAINTS:(.*)', i)
                if altera_constraints:
                    print "Altera CONSTRAINTS = " + altera_constraints.group(1).lstrip()
                    self.altera.constraints = altera_constraints.group(1).lstrip()

                altera_synthesis = re.search('^ALTERA_SYNTHESIS:(.*)', i)
                if altera_synthesis:
                    print "Altera Synthesis = " + altera_synthesis.group(1).lstrip()
                    self.altera.synthesis_files.append(altera_synthesis.group(1).lstrip())


                xilinx_include = re.search('^XILINX_INCLUDE:(.*)', i)
                if xilinx_include:
                    print "Xilinx Include Dirs = " + xilinx_include.group(1).lstrip()
                    self.xilinx.include_dirs.append(xilinx_include.group(1).lstrip())

                xilinx_simulation = re.search('^XILINX_SIMULATION:(.*)', i)
                if xilinx_simulation:
                    print "Xilinx Simulation = " + xilinx_simulation.group(1).lstrip()
                    self.xilinx.simulation_files.append(xilinx_simulation.group(1).lstrip())

                xilinx_fpga = re.search('^XILINX_FPGA:(.*)', i)
                if xilinx_fpga:
                    print "Xilinx Fpga = " + xilinx_fpga.group(1).lstrip()
                    self.xilinx.fpga_model = xilinx_fpga.group(1).lstrip()

                xilinx_netlist = re.search('^XILINX_NETLIST:(.*)', i)
                if xilinx_netlist:
                    print "Xilinx Netlist = " + xilinx_netlist.group(1).lstrip()
                    self.xilinx.netlist = xilinx_netlist.group(1).lstrip()

                xilinx_sdf = re.search('^XILINX_SDF:(.*)', i)
                if xilinx_sdf:
                    print "Xilinx SDF = " + xilinx_sdf.group(1).lstrip()
                    self.xilinx.sdf = xilinx_sdf.group(1).lstrip()

                xilinx_constraints = re.search('^XILINX_CONSTRAINTS:(.*)', i)
                if xilinx_constraints:
                    print "Xilinx CONSTRAINTS = " + xilinx_constraints.group(1).lstrip()
                    self.xilinx.constraints = xilinx_constraints.group(1).lstrip()

                xilinx_synthesis = re.search('^XILINX_SYNTHESIS:(.*)', i)
                if xilinx_synthesis:
                    print "Xilinx Synthesis = " + xilinx_synthesis.group(1).lstrip()
                    self.xilinx.synthesis_files.append(xilinx_synthesis.group(1).lstrip())

                asic_include = re.search('^ASIC_INCLUDE:(.*)', i)
                if asic_include:
                    print "Asic Include Dirs = " + asic_include.group(1).lstrip()
                    self.asic.include_dirs.append(asic_include.group(1).lstrip())

                asic_simulation = re.search('^ASIC_SIMULATION:(.*)', i)
                if asic_simulation:
                    print "Asic Simulation = " + asic_simulation.group(1).lstrip()
                    self.asic.simulation_files.append(asic_simulation.group(1).lstrip())

                asic_fpga = re.search('^ASIC_FPGA:(.*)', i)
                if asic_fpga:
                    print "Asic Fpga = " + asic_fpga.group(1).lstrip()
                    self.asic.fpga_model = asic_fpga.group(1).lstrip()

                asic_netlist = re.search('^ASIC_NETLIST:(.*)', i)
                if asic_netlist:
                    print "Asic Netlist = " + asic_netlist.group(1).lstrip()
                    self.asic.netlist = asic_netlist.group(1).lstrip()

                asic_sdf = re.search('^ASIC_SDF:(.*)', i)
                if asic_sdf:
                    print "Asic SDF = " + asic_sdf.group(1).lstrip()
                    self.asic.sdf = asic_sdf.group(1).lstrip()

                asic_constraints = re.search('^ASIC_CONSTRAINTS:(.*)', i)
                if asic_constraints:
                    print "Asic CONSTRAINTS = " + asic_constraints.group(1).lstrip()
                    self.asic.constraints = asic_constraints.group(1).lstrip()

                asic_synthesis = re.search('^ASIC_SYNTHESIS:(.*)', i)
                if asic_synthesis:
                    print "Asic Synthesis = " + asic_synthesis.group(1).lstrip()
                    self.asic.synthesis_files.append(asic_synthesis.group(1).lstrip())                  
                    
        return

 

################################################################################
#
#
#
################################################################################
if __name__ == '__main__':
    '''
    '''
    print "\n\nTESTING config_file.py"
    C = config_file(file_name="test.cfg", root=".")

