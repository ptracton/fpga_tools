//                              -*- Mode: Verilog -*-
// Filename        : system_controller.v
// Description     : ASIC System Controller
// Author          : Phil Tracton
// Created On      : Fri May 14 09:27:40 2010
// Last Modified By: .
// Last Modified On: .
// Update Count    : 0
// Status          : Unknown, Use with caution!

module system_controller(
			 input wire clk_i,
			 output wire clk_50,
			 output reg clk_1,
			 
			 input wire reset_i,
			 output reg reset_o,
			 output wire locked
			 );

    parameter count_terminal = 25;
    parameter reset_terminal = 255;
    

    //
    // 50 MHZ Clock, it is just the input clock passed through
    //
    assign clk_50 = clk_i;

    //
    // 1 MHZ Clock.  We need to count down the clock and register it to be stable
    //
    reg [5:0] 			     count;
    wire 			     count_done = (count == count_terminal);
    wire 			     clk_1_edge_detected;
    
    always @(posedge clk_i)
      if (reset_i)
	clk_1 <= 1'b0;
      else
	if (clk_1_edge_detected)
	  clk_1 <= ~clk_1;
    
    always @(posedge clk_i)
      if (reset_i)
	count <= 0;
      else
	if (count_done)
	  count <= 'b0;
	else
	  count <= count +1;
    
    positive_edge_detector clk_1_edge(
				      .clk(clk_i),
				      .reset(reset_i),
				      
				      .signal(count_done),
				      .edge_detected(clk_1_edge_detected)
				      );

    //
    // RESET
    //
    reg [7:0] 			     reset_count;
    wire 			     reset_done = (reset_count == reset_terminal);
    assign locked =                  ~reset_o;
    
    always @(posedge clk_i)
      if (reset_i)
	begin
	    reset_count <= 'b0;	    
	    reset_o <= 1'b1;
	end
      else
	if (reset_done)
	  begin
	      reset_o <= 1'b0;
	      reset_count <= 'b0;
	  end
	else
	  reset_count <= reset_count + 1;    
	
    
endmodule // system_controller
