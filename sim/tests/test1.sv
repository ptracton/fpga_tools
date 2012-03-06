# SimVision Command Script (Tue Mar 06 16:31:08 CST 2012)
#
# Version 09.20.s021
#
# You can restore this configuration with:
#
#     simvision -input /data/pace/scratch03/tractp1/hardware/fpga_tools/sim/tests/test1.sv
#


#
# Preferences
#
preferences set toolbar-UserTB0-SrcBrowser {
  usual
  add UserFrame0
  shown 1
  position -row 6 -pos 1 -anchor w
  name {Embedded Software Trace}
}
preferences set toolbar-Standard-WatchWindow {
  usual
  shown 0
}
preferences set toolbar-SimControl-WatchList {
  usual
  hide set_break
  hide vplan
}
preferences set toolbar-SimControl-WaveWindow {
  usual
  hide vplan
}
preferences set toolbar-Windows-WatchWindow {
  usual
  shown 0
}
preferences set user-toolbar-list {SrcBrowser {}}
preferences set toolbar-SimControl-SchematicWindow {
  usual
  hide vplan
}
preferences set toolbar-OperatingMode-WaveWindow {
  usual
  position -pos 5
  name OperatingMode
}
preferences set plugin-enable-groupscope 0
preferences set plugin-enable-interleaveandcompare 0
preferences set toolbar-SimControl-WatchWindow {
  usual
  hide set_break
  hide vplan
  shown 0
}
preferences set toolbar-Edit-WatchWindow {
  usual
  shown 0
}
preferences set toolbar-TimeSearch-WatchWindow {
  usual
  shown 0
}
preferences set toolbar-SimControl-MemViewer {
  usual
  hide vplan
}

#
# Databases
#
database require test -search {
	./test.shm/test.trn
	/data/pace/scratch03/tractp1/hardware/fpga_tools/sim/rtl_sim/run/test1_ncverilog_asic/test.shm/test.trn
}

#
# Groups
#
catch {group new -name {TEST BENCH} -overlay 0}
catch {group new -name DUT -overlay 0}

group using {TEST BENCH}
group set -overlay 0
group set -comment {}
group clear 0 end

group insert \
    test::testbench.any_fail \
    test::testbench.blink \
    test::testbench.clk_tb \
    test::testbench.read_word \
    test::testbench.reset_tb \
    test::testbench.sim_fail \
    test::testbench.sim_pass \
    test::testbench.sim_timeout \
    test::testbench.thread_fail \
    test::testbench.timeout_count \
    test::testbench.timeout_threshold \
    test::testbench.dut.blink

group using DUT
group set -overlay 0
group set -comment {}
group clear 0 end

group insert \
    test::testbench.dut.clk \
    test::testbench.dut.clk_1 \
    test::testbench.dut.clk_50 \
    test::testbench.dut.locked \
    test::testbench.dut.reset_o \
    test::testbench.dut.rst

#
# Cursors
#
set time 0
if {[catch {cursor new -name  TimeA -time $time}] != ""} {
    cursor set -using TimeA -time $time
}

#
# Mnemonic Maps
#
mmap new -reuse -name {Boolean as Logic} -radix %b -contents {
{%c=FALSE -edgepriority 1 -shape low}
{%c=TRUE -edgepriority 1 -shape high}
}
mmap new -reuse -name {Example Map} -radix %x -contents {
{%b=11???? -bgcolor orange -label REG:%x -linecolor yellow -shape bus}
{%x=1F -bgcolor red -label ERROR -linecolor white -shape EVENT}
{%x=2C -bgcolor red -label ERROR -linecolor white -shape EVENT}
{%x=* -label %x -linecolor gray -shape bus}
}

#
# Design Browser windows
#
if {[catch {window new browser -name "Design Browser 1" -geometry 700x500+5+49}] != ""} {
    window geometry "Design Browser 1" 700x500+5+49
}
window target "Design Browser 1" on
browser using "Design Browser 1"
browser set -scope  test::testbench.dut 
browser yview see  test::testbench.dut 
browser timecontrol set -lock 0

#
# Waveform windows
#
if {[catch {window new WaveWindow -name "Waveform 1" -geometry 1914x1059+0+25}] != ""} {
    window geometry "Waveform 1" 1914x1059+0+25
}
window target "Waveform 1" on
waveform using {Waveform 1}
waveform sidebar visibility partial
waveform set \
    -primarycursor TimeA \
    -signalnames name \
    -signalwidth 175 \
    -units ns \
    -valuewidth 75
cursor set -using TimeA -time 0
waveform baseline set -time 0


set groupId0 [waveform add -groups DUT]
waveform hierarchy collapse $groupId0


set groupId0 [waveform add -groups {{TEST BENCH}}]


waveform xview limits 0 10000ns

#
# Waveform Window Links
#

