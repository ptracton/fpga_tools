//                              -*- Mode: Verilog -*-
// Filename        : system_controller.v
// Description     : Altera DE2-115 Demo System Controller
// Author          : Phil Tracton
// Created On      : Fri Dec 23 10:10:52 2011
// Last Modified By: .
// Last Modified On: .
// Update Count    : 0
// Status          : Unknown, Use with caution!

module system_controller(
			 input wire clk_i,
			 output wire clk_50,
			 output wire clk_1,

			 input wire reset_i,
			 output reg reset_o,
			 output wire locked
			 );


   //
   // Count is an 8 bit register used to hold the reset signal high for a time after
   // the reset is done and locked is asserted.  This is done to give us enough time to
   // correctly SYNCHRONOUSLY reset all modules
   //
   reg [7:0] 			count;   
   always @(posedge clk_i)
     begin
	if (~reset_i)
	  count <= 8'h0;
	else if (! locked)
	  count <= 8'h0;	
	else if (count != 8'hFF)
	  count <= count + 1;
     end
   

   // 
   // This is the block that controls the reset logic.  When the count is terminated at 8'hFF reset is released
   // and the system will operate.  Otherwise we hold the system in reset
   //
   always @(posedge clk_i)
     if (~reset_i)
       reset_o <= 1'b1;
     else
       if (count === 8'hFF)
	 reset_o <= 1'b0;
       else
	 reset_o <= 1'b1;   


   //
   // This is a megawizard implementation of the ALTERAPLL module.  c0 is a 50 MHz clock and
   // c1 is a 1 MHz clock.
   //
    altera_demo_pll	altera_demo_pll_inst (
					      .areset ( ~reset_i ),
					      .inclk0 ( clk_i ),
					      .c0 ( clk_50 ),
					      .c1 ( clk_1),
					      .locked ( locked )
					      );
    
   
endmodule // system_controller
