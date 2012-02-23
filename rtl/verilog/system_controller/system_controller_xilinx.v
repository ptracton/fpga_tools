//                              -*- Mode: Verilog -*-
// Filename        : system_controller.v
// Description     : Xilinx System Controller
// Author          : Phil Tracton
// Created On      : Fri May 14 09:27:40 2010
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
    
    parameter count_terminal = 25;
    
    wire 			    clk_ibufg_o;
    wire 			    clk_dcm_o;
    
    wire 			    config_rst, rstin;


    //
    // 1 MHZ Clock.  We need to count down the clock and register it to be stable
    //
    reg 			    clk_1_free;    
    reg [5:0] 			    count_1;
    wire 			    count_done = (count_1 == count_terminal);
    wire 			    clk_1_edge_detected;
    
    always @(posedge clk_i)
      if (reset_i)
	clk_1_free <= 1'b0;
      else
	if (clk_1_edge_detected)
	  clk_1_free <= ~clk_1_free;
    
    always @(posedge clk_i)
      if (reset_i)
	count_1 <= 0;
      else
	if (count_done)
	  count_1 <= 'b0;
	else
	  count_1 <= count_1 +1;
    
    positive_edge_detector clk_1_edge(
				      .clk(clk_i),
				      .reset(reset_i),
				      
				      .signal(count_done),
				      .edge_detected(clk_1_edge_detected)
				      );
        
    
    //
    // Input Buffer for the clock
    //
    IBUFG IBUFG_0(
		  .O(clk_ibufg_o), 
		  .I(clk_i) 
		  );

    //
    // Low skew clock line
    //
    BUFG bufg_clk50(
		    .O (clk_50),
		    .I (clk_dcm_o)
		    );
    
    //
    // Low skew clock line
    //
    BUFG bufg_clk1(
		   .O (clk_1),
		   .I (clk_1_free)
		   );
    
    
    /****************************************************************************
     
     Digital Clock Manager   
     
     ***************************************************************************/
    DCM DCM_0(
	      .CLK0 (clk_dcm_o),
	      .CLK180 (),
	      .CLK270 (),
	      .CLK2X (),
	      .CLK2X180 (),
	      .CLK90 (),
	      .CLKDV (),
	      .CLKFX (),
	      .CLKFX180 (),
	      .LOCKED (locked),
	      .PSDONE (),
	      .STATUS (),
	      .CLKFB (clk_50),
	      .CLKIN (clk_ibufg_o),
	      .DSSEN (1'b0),
	      .PSCLK (1'b0),
	      .PSEN (1'b0),
	      .PSINCDEC (1'b0),
	      .RST (rstin)
	      );
    
    // synopsys translate_off
    defparam  DCM_0.CLK_FEEDBACK          = "1X";
    defparam  DCM_0.CLKIN_PERIOD          = 20.000;
    defparam  DCM_0.CLKOUT_PHASE_SHIFT    = "NONE";
    defparam  DCM_0.DESKEW_ADJUST         = "SYSTEM_SYNCHRONOUS";
    //   defparam  DCM_0.DFS_FREQUENCY_MODE    = "LOW";
    defparam  DCM_0.DLL_FREQUENCY_MODE    = "LOW";
    defparam  DCM_0.DUTY_CYCLE_CORRECTION = "TRUE";
    defparam  DCM_0.FACTORY_JF            = 16'h8080;
    defparam  DCM_0.PHASE_SHIFT           = 0;
    defparam  DCM_0.STARTUP_WAIT          = "FALSE";
    // synopsys translate_on  
    //


    
    //
    // RESET 
    //
    // Create the global reset lines.  Delay the output of reset so that the 
    // regular clock is running and we get the reset signal still.
    //

   //
   // Count is an 8 bit register used to hold the reset signal high for a time after
   // the reset is done and locked is asserted.  This is done to give us enough time to
   // correctly SYNCHRONOUSLY reset all modules
   //
   reg [7:0] 			count;   
   always @(posedge clk_ibufg_o)
     begin
	if (reset_i)
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
   always @(posedge clk_ibufg_o)
     if (reset_i)
       reset_o <= 1'b1;
     else
       if (count === 8'hFF)
	 reset_o <= 1'b0;
       else
	 reset_o <= 1'b1;    
    
    //
    // http://www.xilinx.com/support/answers/14425.htm
    // rstin connects to RST pin of DCM 
    assign rstin = (reset_i || config_rst);  
    
    // This is the actual reset circuit that outputs config_rst. It is a four-cycle shift register. 
    FDS flop1 (.D(1'b0), .C(clk_ibufg_o), .Q(out1), .S(1'b0));  
    FD flop2 (.D(out1), .C(clk_ibufg_o), .Q(out2));  
    FD flop3 (.D(out2), .C(clk_ibufg_o), .Q(out3));  
    FD flop4 (.D(out3), .C(clk_ibufg_o), .Q(out4));  
    
    //config_rst will be asserted for 3 clock cycles. 
    assign config_rst = (out1 | out2 | out3 | out4);
    
endmodule // system_controller
