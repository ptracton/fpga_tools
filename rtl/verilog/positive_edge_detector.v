//                              -*- Mode: Verilog -*-
// Filename        : positive_edge_detector.v
// Description     : Altera DE2-115 Demo
// Author          : Phil Tracton
// Created On      : Fri Dec 23 10:31:52 2011
// Last Modified By: .
// Last Modified On: .
// Update Count    : 0
// Status          : Unknown, Use with caution!


module positive_edge_detector(
			      input wire clk,
			      input wire reset,

			      input wire signal,
			      output wire edge_detected
			      );



   //
   // Hold the input signal for a clock cycle.  The difference between last and signal
   // can be used to determine if an edge has happened
   //
   reg 				     last;
   always @(posedge clk)
     if (reset)
       last <= 1'b0;
     else
       last <= signal;


   //
   // If the current signal is high and the last sampled version is low, then we have a
   // rising edge condition
   //
   assign 			     edge_detected = (!last) & signal;

   
endmodule // positive_edge_detector
