
module top(
	   input wire clk,
	   input wire rst,

	   output reg[7:0] blink
	   );


    wire 	      clk_50, clk_1;
    wire 	      reset_o;
    wire 	      locked;
    
    system_controller sys_con(
			      .clk_i(clk),
			      .clk_50(clk_50),
			      .clk_1(clk_1),
			      
			      .reset_i(rst),
			      .reset_o(reset_o),
			      .locked(locked)
			      );

    always @(posedge clk_50)
      if (reset_o)
	blink <= 8'b0;
      else
	if (locked)
	  blink <= blink +1;
	else
    	  blink <= 8'b0;
    
    
    
endmodule // top
