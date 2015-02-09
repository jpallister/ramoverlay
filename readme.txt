RAM Overlay Optimizer
=====================

This virtual machine has the scripts and toolchains necessary to run the optimization set up. The final binary needs to be run on a board hooked up to a energy measurement device for evaluation, however the statistics for amount of code moved into RAM, number of basic blocks in RAM, cycle estimation can been seen when running the script.

On the desktop, the ramoverlay folder contains the scripts to apply the optimization. The datasets folder contains the data gathered from applying this optimization to various benchmarks at various optimization levels. The tools directory contains a version of qemu which will simulate for the Cortex-M3.

The username and password for this virtual machine are both: ae


What the script does
--------------------

The optimization should be able to be applied to any binary compiled in a single directory with a standard makefile (that accepts CFLAGS). The script accepts the location of the directory. The optimization is applied by partially compiling the files, to get intermediary assembly files. These files are then parsed, a CFG & call graph are constructed. Information is extracted from this and passed to the ILP solver, which informs which basic blocks should be in RAM and which basic blocks should be instrumented. The assembly file is then modified to make these changes, placing all RAM basic blocks in the .data section (so that they are automatically loaded by the crt startup). 


Obtaining actual basic block frequencies
----------------------------------------

Actual basic block frequencies can be given to the optimization using the -i option which specifies a file relative to the benchmark directory. This file contains a list of entries of the form "filename.s:linenumber hits" for each basic block (where linenumber is the line the basic block starts on in the file). These files have be created for 10 of the benchmarks and are present in the benchmark directories (e.g. output_iters.O1), since the computation time can be large.

A script sim_all.py is provided to generate these frequencies via simulation. This uses a python script inside gdb to place a breakpoint on each basic block and count the number of hits.


Benchmarks
----------

A copy of the BEEBS benchmark suite is provided, configured and ready for use. Each benchmark has a directory under beebs_build/stm32vldiscovery/src/*.


Example usage
-------------

Apply optimization to 2dfir
    python rammanager.py beebs_build/stm32discovery/src/2dfir -s

Apply optimization to 2dfir, using max 100 bytes of RAM
    python rammanager.py beebs_build/stm32discovery/src/2dfir -s -m 100

Apply optimization to 2dfir, using allowing up to 10% extra execution time
    python rammanager.py beebs_build/stm32discovery/src/2dfir -s -t 1.1

Apply optimization to 2dfir, compile at O2
    python rammanager.py beebs_build/stm32discovery/src/2dfir -s -f "-O2"

Apply optimization to 2dfir, compile at O1, use exact basic block iterations
    python rammanager.py beebs_build/stm32discovery/src/2dfir -s -f "-O1" -i output_iters.O1



Requirements
------------

Necessary to apply the opimization:
 - ARM Cortex-M3 toolchain
        sudo apt-get install gcc-arm-none-eabi
 - docopt, pexpect, lockfile
        sudo apt-get install python-pip
        sudo pip install docopt, pexpect, lockfile
 - graphviz
        sudo apt-get install graphviz
 - GLPK
        sudo apt-get install glpk-utils


Necessary to simulate, to get basic block freqencies
 - ARM GDB
        sudo apt-get install gdb-arm-none-eabi
 - STM32 QEMU
        sudo apt-get build-dep qemu
        git clone http://github.com/beckus/qemu_stm32
        cd qemu_stm32
        ./configure
        sudo make all install

