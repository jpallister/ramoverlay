#!/usr/bin/python
import gdb
import re
import collections
import os
import time
from subprocess import Popen

port= (os.getpid()+2000) % 62535 + 2000

def backgroundProc(cmd):
    os.system("screen -r gdbqemu{} -X quit".format(port))
    os.system("screen -S gdbqemu{} -d -m bash".format(port))
    os.system("screen -r gdbqemu{} -X screen ".format(port)+cmd)

def killBackground(p):
    os.system("screen -r gdbqemu{} -X quit".format(port))

def getExecDir():
    obj = gdb.objfiles()[0]
    return os.path.dirname(obj.filename)

def findSources():
    s = gdb.execute("info sources", to_string=True)

    edir = getExecDir()
    sources = []

    for line in re.split(',|\n',s):
        if edir in line:
            sources.append(line.strip())

    return sources


def getInsn(s):
    r = r'\s*(?:=>)?\s*0x[a-f0-9]+\s*<[^>]*>:\s*(.+)$'

    m = re.match(r, s)

    if m is None:
        print "No match:", s
        return None

    return m.group(1)

def isBranch(s):
    insn = getInsn(s)

    if insn is None:
        return False

    op = insn.split()[0]

    if len(insn.split()) > 1:
        operands = insn.split()[1]
    else:
        operands = None

    if '.' in op:
        op = op.split('.')[0]

    if op[:3] in ["ldr", "mov"] and operands.strip()[:2] == "pc":
        return True

    if op in ["pop"] and "pc" in operands:
        return True

    return op in ["b", "bgt", "ble", "blt", "bne", "bge", "beq",
        "bls", "bhi", "bcc", "bcs", "bmi", "bpl", "bx", "blx", "bl", "cbnz", "cbz"]

def isConditional(s):
    insn = getInsn(s)

    if insn is None or not isBranch(s):
        return False

    op = insn.split()[0]

    if op[-2:] in ["gt", "le", "lt", "ne", "ge", "eq", "ls", "hi", "cc", "cs", "mi", "pl"]:
        return True
    return False

def getValue(v):
    s = gdb.execute("p/x "+v, to_string=True)
    return int(s.split('=')[1].strip()[2:], 16)

bps = {}

def setupBreakpointsFromFile(fname, sname):
    global bps

    for lineno, line in enumerate(open(fname).xreadlines()):
        if "# break" in line:
            ln = line[8:]
            s = gdb.execute("break "+sname+":"+str(lineno+1), to_string=True)
            bp_n = s.split()[1]

            bps[bp_n] = ln.strip()
            gdb.execute("ignore "+bp_n+" 100000000", to_string=True)


def parseBreakpointResults():
    global bps

    bp_count = {}

    for bp in bps.keys():
        res = gdb.execute("info break "+bp, to_string=True)

        r = res.split('\n')

        if len(r) < 3:
            bp_count[bps[bp]] = 0
        else:
            r = r[2]

        m = re.match(r'\s*breakpoint already hit (\d+)', r)

        if m is None:
            bp_count[bps[bp]] = 0
        else:
            bp_count[bps[bp]] = int(m.group(1))

    return bp_count


qemu = backgroundProc("qemu-system-arm -gdb tcp::{} -M stm32-p103 -nographic -kernel ".format(port)+gdb.objfiles()[0].filename)

try:
    print "Initialising..."
    gdb.execute("set confirm off")
    gdb.execute("set height 0")
    gdb.execute("delete breakpoints", to_string=True)
    # gdb.execute("file "+fname, to_string=True)
    gdb.execute("tar ext :{}".format(port), to_string=True)
    gdb.execute("load", to_string=True)
    gdb.execute("break exit", to_string=True)


    fdir = getExecDir()
    output_iters = fdir + "/output_iters"
    files = findSources()

    print "Exec dir:", fdir

    print "Creating breakpoints..."

    for f in files:
        print "  ", os.path.basename(f)
        setupBreakpointsFromFile(f, os.path.basename(f))

    print "Running benchmark..."
    start = time.time()
    res = gdb.execute("continue", to_string=True)
    end = time.time()
    print "   Simulated for {:.0f} seconds".format(end-start)

    print "Parsing results..."

except Exception as e:
    print "\nException:",e
except KeyboardInterrupt:
    print "\nKeyboard interrupt\n"
finally:
    gdb.execute("monitor quit", to_string=True)
    gdb.execute("disconnect", to_string=True)
    killBackground(qemu)

    bp_count = parseBreakpointResults()

    f = open(output_iters, "w")
    for bp, cnt in sorted(bp_count.items()):
        print bp, cnt
        f.write("{} {}\n".format(bp,cnt))
    f.close()

