import pexpect
import tempfile, os, os.path
import re
import cPickle, atexit
from lockfile import FileLock

cache = {}
if os.path.exists(os.path.expanduser("~/.asmsize.pickle")):
    f = open(os.path.expanduser("~/.asmsize.pickle"))
    cache = cPickle.load(f)
    f.close()

def save():
    global cache
    f = open(os.path.expanduser("~/.asmsize.pickle"),"w")
    cPickle.dump(cache,f)
    f.close()
    print "Saved instruction cache"

atexit.register(save)

preamble = """
    .syntax unified
    .cpu cortex-m3
    .fpu softvfp
    .eabi_attribute 20, 1
    .eabi_attribute 21, 1
    .eabi_attribute 23, 3
    .eabi_attribute 24, 1
    .eabi_attribute 25, 1
    .eabi_attribute 26, 1
    .eabi_attribute 30, 6
    .eabi_attribute 34, 1
    .eabi_attribute 18, 4
    .thumb
"""

def findSize(insn, b_dest=None):
    global cache

    if insn in cache:
        return cache[insn]

    t = tempfile.NamedTemporaryFile(delete=False)
    t.write(preamble+"\n")
    t.write(insn+"\n")
    if b_dest is not None:
        t.write("nop\nnop\nnop\nnop\n"+b_dest+":\n")
    t.close()

    d = os.getcwd()
    newd, name = t.name.rsplit("/", 1)
    os.chdir(newd)

    res = pexpect.run("arm-none-eabi-gcc -c -mthumb -mcpu=cortex-m3 -x assembler {}".format(t.name), withexitstatus=True)
    if res[1] != 0:
        raise RuntimeError(res[0]+"\n"+insn)
    out =  pexpect.run("arm-none-eabi-objdump -d {}.o".format(t.name))

    os.chdir(d)

    size = 0

    for l in out.split('\n'):
        m = re.match(r"\s*[a-f0-9]+:\s*([a-f0-9 ]+)", l)

        if m is not None:
            size = len(m.group(1)) - m.group(1).count(' ')
            # print l.strip(), size/2
            size /= 2
            break

    os.unlink(t.name)

    cache[insn] = size

    return size

