
initial
  begin
      sim_pass <= 1'b0;
      
      $display("TEST1 @ %d", $time);
      repeat(1000) @(clk_tb);

      sim_pass <= 1'b1;
      
  end
    