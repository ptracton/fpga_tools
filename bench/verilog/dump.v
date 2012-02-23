//                              -*- Mode: Verilog -*-
// Filename        : dump.v
// Description     : Dump vcd signals
// Author          : Phil Tracton
// Created On      : Sun Nov 27 14:04:12 2011
// Last Modified By: .
// Last Modified On: .
// Update Count    : 0
// Status          : Unknown, Use with caution!


module dump;
   
   initial
     begin
`ifdef NCVERILOG
	$shm_open("test.shm");
	$shm_probe(testbench, "MAC");
`else	
	$dumpfile("dump.vcd");
	$dumpvars(0, testbench);
`endif
	
     end // initial begin
   
   
endmodule // test_top