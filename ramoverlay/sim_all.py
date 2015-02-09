import os
import rammanager
import sys, traceback

opt_levels = ["O0", "O1", "O2", "O3", "Os"]
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

for b in benchmarks:
    for o in opt_levels:
        if os.path.exists("beebs_build/stm32vldiscovery/src/{}/output_iters.{}".format(b,o)):
            print "Skipping",b,o
            continue

        print "Simulating",b,"at",o

        os.chdir("beebs_build/stm32vldiscovery/src/"+b)

        try:
            cost,cycles,totalram = rammanager.main(compile=True,files=sources[b], model=model, cflags="-"+o, maxram=0, solve=True, max_cycle_factor=10)

            os.chdir(base_dir)

            os.system("arm-none-eabi-gdb -ex \"source sim.py\" -ex \"quit\" beebs_build/stm32vldiscovery/src/{0}/{0}".format(b))
            os.system("cp beebs_build/stm32vldiscovery/src/{0}/output_iters beebs_build/stm32vldiscovery/src/{0}/output_iters.{1}".format(b, o))

        except Exception, e:
            print "Had an exception while trying to RAM:", e
            traceback.print_tb(sys.exc_info()[2])
            os.chdir(base_dir)
