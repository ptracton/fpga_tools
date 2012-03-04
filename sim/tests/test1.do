onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/clk_tb
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/reset_tb
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/blink
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/read_word
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/sim_pass
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/sim_timeout
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/sim_fail
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/thread_fail
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/any_fail
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/timeout_count
add wave -noupdate -expand -group {TEST BENCH} -radix hexadecimal /testbench/timeout_threshold
add wave -noupdate -expand -group DUT -radix hexadecimal /testbench/dut/clk
add wave -noupdate -expand -group DUT -radix hexadecimal /testbench/dut/rst
add wave -noupdate -expand -group DUT -radix hexadecimal /testbench/dut/blink
add wave -noupdate -expand -group DUT -radix hexadecimal /testbench/dut/clk_50
add wave -noupdate -expand -group DUT -radix hexadecimal /testbench/dut/clk_1
add wave -noupdate -expand -group DUT -radix hexadecimal /testbench/dut/reset_o
add wave -noupdate -expand -group DUT -radix hexadecimal /testbench/dut/locked
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ps} 0}
configure wave -namecolwidth 298
configure wave -valuecolwidth 66
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ps
update
WaveRestoreZoom {9968670 ps} {9998690 ps}
