
`include "timescale.v"
module testbench;

    //
    // Free Running 50 MHz clock
    //
    parameter _clk_50mhz_high = 10,
		_clk_50mhz_low  = 10,
		_clk_50mhz_period = _clk_50mhz_high + _clk_50mhz_low;
    
    reg clk_tb;	
    
    initial
      begin
	  clk_tb <= 'b0;
	  forever
	    begin
		#(_clk_50mhz_low)  clk_tb = 1;
		#(_clk_50mhz_high) clk_tb = 0;	     
	    end	
      end
    
    //
    // Global Asynch reset, KEY[3] on the board is ACTIVE LOW
    //
    reg 	     reset_tb; 
`ifdef ALTERA  
    initial
      begin
	  reset_tb = 1;
	  #1    reset_tb = 0;
	  #2000 reset_tb = 1;
      end
`else    
    initial
      begin
	  reset_tb = 0;
	  #1    reset_tb = 1;
	  #2000 reset_tb = 0;
      end
`endif // !`ifdef ALTERA

    
    //
    // FPGA to test
    //
    wire [7:0] blink;
    
    top dut(
	    .clk(clk_tb),
	    .rst(reset_tb),
	    
	    .blink(blink)
	    
	    );

  
    //
    // Terminate Test
    //
    reg [31:0] read_word;    
    reg 	sim_pass;
    wire 	sim_timeout;
    reg 	sim_fail;
    reg 	thread_fail;    
    wire 	any_fail;

    integer 	timeout_count;
    integer 	timeout_threshold;

    //
    // If we declare an error or take too long it is a fail
    //
    assign any_fail = sim_fail | sim_timeout | thread_fail;

    //
    // Initialize the test variables and check for command line options
    //
    initial
      begin
	  sim_pass <= 1'b0;
	  sim_fail <= 1'b0;
	  timeout_threshold <= 550000;
	  timeout_count <= 0;
	
	  
	  if ($value$plusargs("TIMEOUT=%d", timeout_threshold))
	    $display("TIMEOUT = %d", timeout_threshold);	

	    
	  
      end

    //
    // Count the number of clocks to make sure we don't go too long
    //
    assign     sim_timeout = timeout_count >= timeout_threshold;   
    always @(posedge clk_tb)
      timeout_count = timeout_count + 1;

    //
    // We passed!
    //
    always @(posedge sim_pass)
      begin
	  $display("*********************************************************");
	  $display("SIM PASSED @ %d", $time);
	  $display("*********************************************************");
	  force testbench.sim_fail = 0;
	  #10 $finish;	  
      end

    //
    // If any of the fail cases get tripped, terminate the sim
    //
    always @(posedge any_fail)
      begin
	  $display("*********************************************************");	
	  if (sim_fail)
	    $display("FAIL: Test Failure at %d",$time);
	  else if (sim_timeout)
	    $display("FAIL: Timeout  at %d",$time);	
	  else
	    $display("FAIL: Unknown Failure at %d",$time);
	  $display("*********************************************************");
	  #10 $finish;
      end // always @ (any_fail)
        
    
    //
    // Dump signals for waveform viewing
    //
    dump dump();
    

    //
    // Include external thread for testing
    //
`include "stimulus.v"
        
endmodule // testbench
