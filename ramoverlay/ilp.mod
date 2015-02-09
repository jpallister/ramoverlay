
set BBs;
set onoff;

param usize{bb in BBs}, integer;
param cyc_cost{bb in BBs}, integer;
param icost_ram{bb in BBs}, integer; # Cost in bytes of instrumenting a block
param icost_cyc{bb in BBs}, integer; # Cost in cycles of instrumenting a block
param icost_cyc_ram{bb in BBs}, integer; # Cost in cycles for a block to be in RAM
param force_ram{bb in BBs}, integer;
param force_flash{bb in BBs}, integer;
param iterations{bb in BBs}, integer;
param successors{bb in BBs, bb2 in BBs}, binary;
param E_flash;
param E_ram;
param spare_ram;
param max_cycle_factor;

var BBs_in_ram{BBs} >=0 binary;

var is_bb_instrumented{BBs} >=0 binary;
var succ_in_ram{bb in BBs, bb2 in BBs}  binary;
var succ_not_in_ram{bb in BBs, bb2 in BBs}  binary;
var max_inst{bb in BBs, bb2 in BBs}  binary;
var max_inst2{bb in BBs, bb2 in BBs}  binary;

var BBs_in_ram_instrumented{BBs} >=0 binary;
var BBs_not_in_ram_instrumented{BBs} >=0 binary;


minimize cost: sum{bb in BBs}
	(
	(
        (cyc_cost[bb] + icost_cyc_ram[bb]) * E_ram * BBs_in_ram[bb] +
        cyc_cost[bb] * E_flash * (1 - BBs_in_ram[bb]) +
        icost_cyc[bb] * E_ram * BBs_in_ram_instrumented[bb] +
	    icost_cyc[bb] * E_flash * BBs_not_in_ram_instrumented[bb]
      )
	  * iterations[bb]
	);

# These two constraints create variables defining whether a bb is instrumented and in ram
# or instrumented and not in ram. This allows the instrumentation cost to be scaled appropriately.
subject to instrument_cost_cons1{bb in BBs}:
    BBs_in_ram_instrumented[bb] >= BBs_in_ram[bb] + is_bb_instrumented[bb] - 1;

subject to instrument_cost_cons2{bb in BBs}:
    BBs_not_in_ram_instrumented[bb] >=  (1 - BBs_in_ram[bb]) + is_bb_instrumented[bb] - 1;

# the block is instrumented if it is in RAM, and its successors is not
subject to instrument_cons1{bb in BBs, bb2 in BBs}:
    is_bb_instrumented[bb] >= max_inst[bb,bb2];

subject to instrument_cons1c{bb in BBs, bb2 in BBs}:
    max_inst[bb,bb2] >= BBs_in_ram[bb] + succ_not_in_ram[bb,bb2] - 1;


# the block is instrumented if it is not in RAM, and its successors is
subject to instrument_cons2{bb in BBs, bb2 in BBs}:
    is_bb_instrumented[bb] >= max_inst2[bb,bb2];

subject to instrument_cons2a{bb in BBs, bb2 in BBs}:
    max_inst2[bb,bb2] >= (1 - BBs_in_ram[bb]) + succ_in_ram[bb,bb2] - 1;


# This constraint checks whether any block jumps to bb (by summing the column of successors)
# If there is not, and we are in RAM, then we need to instrument this block too, because
# it may be possible that we end up executing from this block, without being in RAM.
# E.g. an untranslated function call.
subject to instrument_cons3{bb in BBs}:
    is_bb_instrumented[bb] >= BBs_in_ram[bb] * (1 - sum{bb2 in BBs}(successors[bb2,bb]));

# For now, we make sure that if nothing jumps to the bb, it cant be in ram
subject to no_starts{bb in BBs}:
    BBs_in_ram[bb] <= sum{bb2 in BBs}(successors[bb2,bb]);

# Create variables for successors in ram and not in ram
subject to instrument_cons5a{bb in BBs, bb2 in BBs}:
    succ_in_ram[bb,bb2] = (successors[bb,bb2] * BBs_in_ram[bb2]);

subject to instrument_cons5b{bb in BBs, bb2 in BBs}:
    succ_not_in_ram[bb,bb2] = (successors[bb,bb2] * (1-BBs_in_ram[bb2]));


# This constraint makes sure we can fit into the RAM allocation given
subject to ram_constraint:
	sum{bb in BBs}(BBs_in_ram[bb] * usize[bb] + BBs_in_ram_instrumented[bb] * icost_ram[bb]) <= spare_ram;


# This allows us to restrict the number of cycles executed
subject to cyc_constraint2:
    sum{bb in BBs}( (cyc_cost[bb] + is_bb_instrumented[bb] * icost_cyc[bb] + BBs_in_ram[bb]*icost_cyc_ram[bb])*iterations[bb]) <= sum{bb in BBs}(cyc_cost[bb] * iterations[bb]) * max_cycle_factor;

# In certain circumstance we want to force certain blocks into RAM
subject to force_constraint1{bb in BBs}:
    BBs_in_ram[bb] >= force_ram[bb];
subject to force_constraint2{bb in BBs}:
    BBs_in_ram[bb] <= 1-force_flash[bb];

solve;

printf: "# Base  cost: %.0f\n", sum{bb in BBs}
    (
        (
        cyc_cost[bb] * E_flash
        ) * iterations[bb]
    );

printf: "# Final cost: %.0f\n", sum{bb in BBs}
	(
        (
        (cyc_cost[bb] + icost_cyc_ram[bb]) * E_ram * BBs_in_ram[bb] +
        cyc_cost[bb] * E_flash * (1 - BBs_in_ram[bb]) +
        icost_cyc[bb] * E_ram * BBs_in_ram_instrumented[bb] +
	    icost_cyc[bb] * E_flash * BBs_not_in_ram_instrumented[bb]
        ) * iterations[bb]
	);

printf: "# Base  cycles: %.0f\n", sum{bb in BBs}(cyc_cost[bb]*iterations[bb]);
printf: "# Final cycles: %.0f\n#             / %.0f\n", sum{bb in BBs}( (cyc_cost[bb] + is_bb_instrumented[bb] * icost_cyc[bb]+ BBs_in_ram[bb]*icost_cyc_ram[bb])*iterations[bb]), sum{bb in BBs}(cyc_cost[bb] * iterations[bb]) * max_cycle_factor;
printf: "# xlim: %.3f\n", max_cycle_factor;
printf: "# Base  total size: %.0f\n", sum{bb in BBs}(usize[bb]);
printf: "# Final total size: %.0f\n", sum{bb in BBs}(usize[bb] + is_bb_instrumented[bb] * icost_ram[bb]);
printf: "# Final RAM size: %.0f\n", sum{bb in BBs}(BBs_in_ram[bb] * usize[bb] + BBs_in_ram_instrumented[bb] * icost_ram[bb]);


printf: "# name, size, ram, instrumented\n";
printf{bb in BBs}: "%s, %.0f, %.0f, %.0f\n", bb, usize[bb] + icost_ram[bb]*is_bb_instrumented[bb], BBs_in_ram[bb],is_bb_instrumented[bb];

# printf: "\nsucc_in_ram\n";
# for {bb in BBs}
# {
#     printf{bb2 in BBs}: "%d ", succ_in_ram[bb,bb2];
#     printf: "\n";
# }

# printf: "\nsucc_not_in_ram\n";
# for {bb in BBs}
# {
#     printf{bb2 in BBs}: "%d ", succ_not_in_ram[bb,bb2];
#     printf: "\n";
# }

# printf: "\nmax_inst\n";
# for {bb in BBs}
# {
#     printf{bb2 in BBs}: "%d ", max_inst[bb,bb2];
#     printf: "\n";
# }


# printf: "\nmax_inst2\n";
# for {bb in BBs}
# {
#     printf{bb2 in BBs}: "%d ", max_inst2[bb,bb2];
#     printf: "\n";
# }

data;

set BBs := bb1 bb2 bb3 bb4 bb5;

param usize :=
    bb1   101
    bb2   50
    bb3   40
    bb4   101
    bb5   101;

param iterations :=
	bb1   1
    bb2   10
    bb3   10
	bb4   1
	bb5   1;

param icost_ram :=
    bb1   2
    bb2   2
    bb3   2
    bb4   2
    bb5   2;

param icost_cyc :=
    bb1   5
    bb2   5
    bb3   5
    bb4   5
    bb5   5;

param cyc_cost :=
    bb1 200
    bb2 40
    bb3 40
    bb4 200
    bb5 200;

param force_ram :=
    bb1 0
    bb2 0
    bb3 0
    bb4 0
    bb5 0;

param force_flash :=
    bb1 0
    bb2 0
    bb3 0
    bb4 0
    bb5 0;

# Sucessors is
# [row, col]
# row is from, col is to, i.e. col is a successor of row

param successors : bb1 bb2 bb3 bb4 bb5:=
    bb1   0  1  0  0  0
    bb2   0  0  1  0  0
    bb3   0  0  0  1  0
    bb4   0  0  0  0  1
    bb5   0  0  0  0  0
    ;

param E_flash := 200;
param E_ram := 150;
param spare_ram := 100;
param max_cycle_factor := 1.035;
end;
