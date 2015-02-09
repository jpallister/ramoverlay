Basic Block Overlay Manager
===========================

This constructs a CFG from arm assembly, the instruments the desired basic blocks in such a way that they can be dynamically relocated to memory.

Each RAM basic block is instrumented with labels before and after, so that runtime code can copy it into memory.

Each block which jumps to a target block (and target blocks) has its branches rewritten to perform a jump table lookup first. If the block can 'fall through' into the basic block underneath then the fallthrough is instrumented with a branch, so that the execution can be redirected.


Running
-------

1. Compile the beebs benchmarks required, with -save-temps -ffixed-r5 -DRAM_MANAGER -fstack-usage
2. Run rammanager.py on the assembly file needed
3. Select the basic blocks to go into memory
4. Copy the file.s.out in place of the benchmarks file, assembly and link into benchmark.

