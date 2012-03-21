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
import subprocess
import re

class test_case:
    '''
    '''
    ############################################################################
    def __init__(self, test_name="", tool="", tech=""):

        self.test_name = test_name
        self.test_status = False
        self.tool = tool
        self.tech = tech
        self.sim_dir = self.test_name+"_"+self.tool+"_"+self.tech

    ############################################################################
    def sim_passed(self):
        test_log = self.sim_dir+"/"+self.test_name+".log"
        if os.path.exists(test_log):            
            f = open(test_log)
            lines = f.readlines()
            f.close()
            for i in lines:
                match = re.search("SIM PASSED",i)
                if (match):
                    return True
            else:
                return False

    ############################################################################
    def done(self):

        ## If the simulation complete file is not there, return False
        done = self.sim_dir + "/simulation_complete"        
        if not os.path.exists(done):
            return False        
        
        return True
        
    ############################################################################
    def run(self):
        executable = "run_sim.py"
        process = subprocess.Popen([executable, "--"+self.tool, "--"+self.tech, self.test_name ], shell=False).wait()
        return
    
    ############################################################################
    def status(self):
        if self.done():            
            if self.sim_passed():
                self.test_status = True
            else:
                self.test_status = False
        else:
            self.test_status = False
            
        return self.test_status

    
