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

class fpga:
    '''
    '''

    def __init__(self):

        #
        # Simulation details
        #
        self.simulation_files = []
        self.include_dirs = []
        
        #
        # Synthesis details
        #
        self.synthesis_files = []
        self.fpga_model = ""        
        self.netlist = ""
        self.sdf = ""
        self.constraints = ""

        return

    def __help__(self):
        return "Class fpga: This is just a data containing class for fields in the configuration file"

    def __str__(self):
        return "fpga"
    
################################################################################
#
#
#
################################################################################
if __name__ == '__main__':
    '''
    '''
    f = fpga()
    print f
    help(f)

    
