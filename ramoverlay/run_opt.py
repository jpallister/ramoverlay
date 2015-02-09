"""Run opt

Usage:
    run_opt.py BENCHMARK OPT_STRING...
"""
import docopt
import rammanager
import os, string, sys, traceback

benchmarks = ["2dfir", "blowfish", "crc32", "cubic", "dijkstra", "fdct", "float_matmult", "int_matmult", "rijndael", "sha"]
sources = {
        "2dfir": ["fir2dim.s"],
        "blowfish": ["bf_cfb64.s", "bf.s", "bf_enc.s", "bf_skey.s"],
        "crc32": ["crc_32.s"],
        "cubic": ["cubic.s", "basicmath_small.s"],
        "dijkstra": ["dijkstra_small.s"],
        "fdct": ["fdct.s"],
        "float_matmult": ["matmult.s"],
        "int_matmult": ["matmult.s"],
        "rijndael": ["aes.s", "aesxam.s"],
        "sha": ["sha.s", "sha_driver.s"]
        }

base_dir = os.getcwd()
model = "ilp.mod"
model = os.getcwd() + "/" + model

def run_opt_comparison(benchmark, opt_string, desc):
    src = "beebs_build/stm32vldiscovery/src/"
    temp_dir = "/panfs/panasas01/cosc/jp8257/data/ramoverlay/" + desc 

    os.system("mkdir -p "+temp_dir)
    os.system("cp -r beebs /panfs/panasas01/cosc/jp8257/data/ramoverlay/{desc}".format(**locals()))
    os.system("cp -r beebs_build /panfs/panasas01/cosc/jp8257/data/ramoverlay/{desc}".format(**locals()))

    temp_dir = temp_dir + "/beebs_build/stm32vldiscovery/src/" + benchmark 

    try:
        os.chdir(temp_dir)
        cost,cycles,ram = rammanager.main(compile=True,files=sources[benchmark], model=model, cflags="-O3 "+opt_string, maxram=0, solve=True, max_cycle_factor=10)

        os.chdir(base_dir)
        os.system("arm-none-eabi-gdb -ex \"source sim.py\" -ex \"quit\" {temp_dir}/{benchmark}".format(**locals()))
    
        os.chdir(temp_dir)
        opt_cost,opt_cycles,opt_ram = rammanager.main(compile=False,files=sources[benchmark], model=model, cflags="-O3 "+opt_string, maxram=2000, solve=True, max_cycle_factor=10,iteration_file="output_iters")
        base_cost,base_cycles,ram = rammanager.main(compile=False,files=sources[benchmark], model=model, cflags="-O3 "+opt_string, maxram=0, solve=True, max_cycle_factor=10,iteration_file="output_iters")
    except Exception, e:
        print "Had an exception while trying to RAM:", e
        traceback.print_tb(sys.exc_info()[2])
    finally:
        os.chdir(base_dir)

    return base_cost, base_cycles, opt_cost, opt_cycles, opt_ram

if __name__=="__main__":
    arguments = docopt.docopt(__doc__)

    f = open("gcc_4.8.2_opt_list")
    opts = map(string.strip, f.readlines())

    for o in arguments['OPT_STRING']:
        optstr = ""

        for v, opt in zip(o, opts):
            if v == "1":
                optstr += "-f" + opt + " "
            else:
                optstr += "-fno-" + opt + " "

        print "Testing opt string:", o, "\n",optstr

        r = run_opt_comparison(arguments['BENCHMARK'], optstr, o)
        print r

        f = open("ffd_results/"+arguments['BENCHMARK']+ "_" + o, "w")
        f.write("{}, {}, {}, {}, {}\n".format(*r))
        f.close()

        


