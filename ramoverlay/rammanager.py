"""Instrument basic blocks and copy them to RAM.

Usage:
    rammanager.py [options] [--bb BB]... DIRECTORY
    rammanager.py -h

Options:
    -h --help           Show this message
    -s --solve          Invoke glpsol to get a list of basic blocks for memory
    -m --maxram RAM     Specify the maximum amount of RAM to allow for basic
                        blocks. If RAM is compute and -c is specified, the
                        -fstack-usage option is used to find the stack usage.

                        This hits problems when the stack usage is dynamic.

    -t --maxtime TIME   This sets a maximum % increase in the time allowed.
                        For example, if this is set to 2, the total number of
                        cycle is allowed to double. [default: 1.5]

    -f --flags FLAGS    CFLAGS to pass to make, if --compile is set [default: ]

    --bb BB             Place this BB in RAM. Of the form file:lineno
    -i --iterations IF  Use this file to denote the number of times each
                        basic block is executed

    -e --estimate EST   Use E iterations per loop as the estimate. [default: 10]

"""

from docopt import docopt

import arm
import cfg
import logging, logging.config
import os,os.path,sys,glob
import itertools, re
import pexpect, string, collections
from copy import copy

# logging.config.fileConfig("/home/james/.pylogging.conf")

safe_register = "r5"

# Load instructions from an assembly file, and search through them to
# find call instructions
def loadInstructions(fname):
    insns, lines, calls = arm.loadInstructions(fname)

    call_dests = []

    for insn in insns:
        if insn.isCall():
            call_dests.append(insn.branchDestination())
        insn.file = fname

    return insns, lines, call_dests+calls

# Create a CFG from the list of instructions. Use call_sites as a
# starting point to construct the functions
def constructCFGs(insns, call_sites=[]):
    overall_cfg = cfg.CFG()
    overall_cfg.construct_new(insns, call_sites)

    cfgs = overall_cfg.partition()

    for c in cfgs:
        for bb in c.basicblocks:
            bb.cfg = c
            bb.iterations = 1

    return cfgs

def drawCFGs(cfgs, prefix=""):
    if not os.path.exists("cfgs"):
        os.mkdir("cfgs")
    for i, cfg in enumerate(cfgs):
        print "\tDrawing cfg", i, prefix
        cfg.findLoops()
        cfg.dumpDot(open("cfgs/cfg{}_{}.dot".format(prefix,i), "w"))
        os.system("dot -Tpng cfgs/cfg{0}_{1}.dot > cfgs/cfg{0}_{1}.png".format(prefix, i))

def buildCallGraph(cfgs):
    edges = []

    print "Building the callgraph"

    cur_fn = ""

    unknown_labels = set([])
    # Perhaps this could be written better
    # Precompute list of destinations, and lookup label
    for c in cfgs:
        for bb in c.basicblocks:

            # Purely for display
            if bb.instructions[0].label and bb.instructions[0].label[0] != '.':
                cur_fn = bb.instructions[0].label

            for insn in bb.instructions:
                if not insn.isCall() and not insn.markedAsCall:
                    continue
                src = bb
                dest_label = insn.branchDestination()
                dest_bb = None

                for c2 in cfgs:
                    for bb2 in c2.basicblocks:
                        if bb2.instructions[0].label == dest_label:
                            dest_bb = bb2

                if dest_bb is None:
                    unknown_labels.add(dest_label)
                    continue

                sb = cfg.findStartingBlocks(c.basicblocks)[0]
                print "\tAdding edge ", sb.instructions[0].file,cur_fn, "->",dest_bb.instructions[0].file, dest_label

                edges.append((src,dest_bb))
    if unknown_labels:
        print "\tUnfound labels in callgraph:",list(unknown_labels)

    return edges

def findRootCFG(cfgs, edges):
    cfglist = copy(cfgs)

    for e_from, e_to in edges:
        for c in cfgs:
            if e_to in c.basicblocks and c in cfglist:
                del cfglist[cfglist.index(c)]

    if len(cfglist) > 1:
        print "There are more than 1 root CFGs..."
        for c in cfglist:
            starts = cfg.findStartingBlocks(c.basicblocks)
            print "   ",starts[0].instructions[0].label

    return cfglist

def estimateIterations(root, cfgs, edges, estimate, processed_bbs=[], base_iterations=1, depth=0):

    if depth > 5:
        print "Recursion limit"
        return

    sb = cfg.findStartingBlocks(root.basicblocks)[0]
    print "  "*depth+"In fn", sb.instructions[0].label, sb.instructions[0].file

    root.findLoops()

    for bb in root.basicblocks:

        # Get the loop depth of the current basic block
        cols = []
        lh = root.getLoopHeaders(bb)
        if bb in root.loop_headers:
            lh = [bb] + lh

        for header in lh:
            if header in root.loop_headers:
                i = root.loop_headers.index(header)
                cols.append(i)

        if bb in lh:
            iter_count = estimate ** (len(cols)+1) * (estimate+1) * base_iterations
        else:
            iter_count = estimate ** len(cols) * base_iterations
        bb.iterations = max(bb.iterations, iter_count)

        for e in edges:
            # print e[0].instructions[0].label
            if e[0] == bb:
                # if e[0] in processed_bbs:
                #     print "Recursive CFG found?!"
                #     continue

                found = False
                for c in cfgs:
                    if e[1] in c.basicblocks:
                        estimateIterations(c, cfgs, edges, estimate, processed_bbs+[e[1]], bb.iterations, depth+1)
                        found = True

                if not found:
                    print "Could not find destination CFG?!"

def loadIterations(file_cfgs, fname):
    print "Loading iterations from file"
    for line in open(fname).readlines():
        parts = line.split()

        if ':' not in parts[0]:
            delim = "_"
        else:
            delim = ":"

        f_iter = parts[0].rsplit(delim,1)[0]
        f_line = parts[0].rsplit(delim,1)[1]

        if f_iter not in file_cfgs:
            print "Error, iteration file specifies file:",f_iter

        found = False
        for c in file_cfgs[f_iter]:
            for bb in c.basicblocks:
                if bb.instructions[0].lineno == int(f_line):
                    found = True
                    bb.iterations = int(parts[1])
        if not found:
            print "Error could not find basic block:",parts[0]



def markRAMBB(bb):
    insn = bb.getTailInsn()
    first_insn = bb.instructions[0]

    precode = ".section ramoverlay, \"x\"\n.align 2"
    postcode = ".text\n.align 2"

    changes = []

    # Iterate through the instructions, and look for calls
    # If we find a call, replace with a relative load
    for cur_insn in bb.instructions:
        if cur_insn.isCall():
            code_add = "    ldr r5, ={}\n" \
                       "    blx r5".format(cur_insn.branchDestination())
            changes.append({"code_replace": (cur_insn.lineno, code_add)})
        if cur_insn.operator == "adr":
            parts = cur_insn.operands.split(',')
            code_add = "    ldr {}, ={}".format(parts[0], parts[1].strip())
            changes.append({"code_replace": (cur_insn.lineno, code_add)})


    changes.append({"code_after": (insn.lineno, postcode)})
    changes.append({ "code_before": (first_insn.lineno, precode)})

    return changes

def transformReferences(bb):
    changes = []
    for cur_insn in bb.instructions:
        if cur_insn.operator == "ldr" and '[' not in cur_insn.operands and '=' not in cur_insn.operands:
            code_rm =  (cur_insn.lineno,)
            parts = cur_insn.operands.split(',')
            code_add = "    ldr {0}, ={1}\n    ldr {0}, [{0}]".format(parts[0], parts[1].strip())
            changes.append({"code_replace": (cur_insn.lineno, code_add)})

    ti = bb.getTailInsn()
    if ti.isBranch() and ti.isUnconditional() and not ti.isCall():
        changes.append({"code_after":(ti.lineno, ".ltorg")})

    changes.append({"code_before": (bb.instructions[0].lineno, ".align 2")})

    return changes

def breakpointBB(bb):
    changes = []

    bp_name = str(bb.instructions[0].file) + ":" + str(bb.instructions[0].lineno)

    if bb.instructions[0].label is False:
        changes.append({"code_before":(bb.instructions[0].lineno, "# break "+bp_name)})
    else:
        changes.append({"code_after":(bb.instructions[0].lineno, "# break "+bp_name)})
    return changes

def instrumentBB(bb):
    global safe_register

    print "\tInstrumenting BB: {}:{}".format(bb.instructions[0].file, bb.instructions[0].lineno)

    insn = bb.getTailInsn()

    if insn.isBranch() and insn.branchDestination() is None:
        print "Possible FATAL ERROR: not sure how to instrument this basic block"
        return []

    branch2reg = {
        "b" : "bx",
   #     "bl" : "blx",
        "bgt" : "bx",
        "ble" : "bx",
        "blt" : "bx",
        "bne" : "bx",
        "bge" : "bx",
        "beq" : "bx",
        "bls" : "bx",
        "bhi" : "bx",
        "bcc" : "bx",
        "bcs" : "bx",
        "bmi" : "bx",
        "bpl" : "bx",
        }
    inverse_cond = {
        "eq" : "ne",
        "ne" : "eq",
        "ge" : "lt",
        "lt" : "ge",
        "gt" : "le",
        "le" : "gt",
        "ls" : "hi",
        "hi" : "ls",
        "cc" : "cs",
        "cs" : "cc",
        "mi" : "pl",
        "pl" : "mi",
        }

    destination = insn.branchDestination()
    reg = safe_register

    if insn.operator in ["cbnz", "cbz"]:
        b_insn = "bx"
        if insn.operator == "cbnz":
            cond_code = "ne"
        else:
            cond_code = "eq"
        inv_cond_code = inverse_cond[cond_code]

        creg = insn.operands.split(',')[0]

        # 10 byte, 8 cycles
        code = "    # cbz/cbnz conditional indirect\n" \
               "    cmp {creg}, #0\n" \
               "    ite {cond_code}\n" \
               "    ldr{cond_code} {reg}, ={destination}+1\n" \
               "    ldr{inv_cond_code} {reg}, =fallthrough_{insn.lineno}+1\n" \
               "    {b_insn} {reg}\n" \
               "    .ltorg".format(**locals())

        ft = "fallthrough_{insn.lineno}:".format(**locals())
        fallthrough = [{"code_before":(insn.lineno+1, ft)}]
    elif insn.isUnconditional():
        b_insn = branch2reg[insn.operator]

        # 2 bytes, 4 cycles
        code = "    # Unconditional indirect\n" \
               "    ldr pc, ={destination}+1\n" \
               "    .ltorg" \
               .format(**locals())
        fallthrough = []

    elif not insn.isBranch():
        # 2 bytes, 4 cycles
        code = "    # Fallthrough indirect\n" \
               "    ldr pc, =fallthrough_{insn.lineno}+1\n" \
               "    .ltorg".format(**locals())

        ft = "fallthrough_{insn.lineno}:".format(**locals())
        fallthrough = [{"code_before":(insn.lineno+1, ft)}]

    else: # Conditional
        b_insn = branch2reg[insn.operator]
        cond_code = insn.operator[-2:]
        inv_cond_code = inverse_cond[cond_code]
        # 6 bytes, 4 cycles
        code = "    # Conditional indirect\n" \
               "    ite {cond_code}\n" \
               "    ldr{cond_code} {reg}, ={destination}+1\n" \
               "    ldr{inv_cond_code} {reg}, =fallthrough_{insn.lineno}+1\n" \
               "    {b_insn} {reg}\n.ltorg".format(**locals())

        ft = "fallthrough_{insn.lineno}:".format(**locals())
        fallthrough = [{"code_before":(insn.lineno+1, ft)}]

    changes = [{"code_after": (insn.lineno, code)}]

    if insn.isBranch():
        changes[0]["code_remove"] = (insn.lineno,)

    changes.append({"code_before":(bb.instructions[0].lineno,"# INSTRUMENTED "+str(bb.instructions[0].lineno))})

    return changes, fallthrough

def applyChanges(lines, changes):
    lines_out = []

    for current_line, l in enumerate(lines):
        write_line = True
        for c in changes:
            if "code_remove" in c:
                if current_line == c['code_remove'][0]:
                    write_line = False

        for c in changes:
            if "code_before" in c:
                if current_line == c['code_before'][0]:
                    for new_l in c['code_before'][1].split('\n'):
                        lines_out.append(new_l + "\n")

        for c in changes:
            if "code_replace" in c:
                if current_line == c['code_replace'][0]:
                    for new_l in c['code_replace'][1].split('\n'):
                        lines_out.append(new_l + "\n")
                    write_line = False
        if write_line:
            lines_out.append(l)

        for c in changes:
            if "code_after" in c:
                if current_line == c['code_after'][0]:
                    for new_l in c['code_after'][1].split('\n'):
                        lines_out.append(new_l + "\n")

    lines_out.append(".data\n")

    for c in changes:
        if "data_add" in c:
            for new_l in c['data_add'].split('\n'):
                lines_out.append(new_l + "\n")

    return lines_out

def solveForIterationCount(file_cfgs, cfgs, model):
    fname = "iterations.data"
    f = open(fname, "w")

    all_bbs = list(itertools.chain(*map(lambda x: x.basicblocks, cfgs)))

    bb_names = []
    for bb in all_bbs:
        insn0 = bb.instructions[0]
        bb_names.append("{}_{:04d}".format(insn0.file,insn0.lineno))

    bb_map = dict(zip(bb_names, all_bbs))
    maxname = max(map(len, bb_names))

    bb_names.sort()


    # Output list of beasic blocks first
    f.write("set BBs := {};\n\n".format(" ".join(bb_names)))

    # output initial
    f.write("param iterations_initial :=\n")
    for bb_name, bb in zip(bb_names, all_bbs):
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, 0))
    f.write(";\n\n")

    loop_exits = collections.defaultdict(int)

    for bb_name in bb_names:
        cur_bb = bb_map[bb_name]
        dests = cur_bb.destinations

        lh = cur_bb.getLoopHeaders()
        bb_depth = len(lh)

        if len(dests) == 2:
            d0_depth = len(dests[0].getLoopHeaders())
            d1_depth = len(dests[1].getLoopHeaders())

            if d0_depth < bb_depth:
                for i in range(bb_depth - d0_depth):
                    loop_exits[lh[i]] += 1
                    print "Loop exit @{} for loop@{}".format(cur_bb.instructions[0].lineno, lh[i].instructions[0].lineno)
            if d1_depth < bb_depth:
                for i in range(bb_depth - d1_depth):
                    loop_exits[lh[i]] += 1
                    print "Loop exit @{} for loop@{}".format(cur_bb.instructions[0].lineno, lh[i].instructions[0].lineno)



    print loop_exits

    # Output bb to bb probability
    f.write("param branch_prob : {} :=\n".format(" ".join(bb_names)))
    for bb_name in bb_names:
        f.write("\t{1: <{0}}\t\t".format(maxname, bb_name))
        dests = bb_map[bb_name].destinations
        cur_bb = bb_map[bb_name]

        # Find the inner most loop for this basic block
        lh = cur_bb.getLoopHeaders()
        bb_depth = len(lh)

        # Work out if both destinations are in the same loop
        same = True
        if len(dests) == 2:
            d0_depth = len(dests[0].getLoopHeaders())
            d1_depth = len(dests[1].getLoopHeaders())

            if d0_depth < bb_depth or  d1_depth < bb_depth:
                same = False

        for bb_name2 in bb_names:
            dest_bb = bb_map[bb_name2]

            # Find the inner most loop for this basic block
            dest_depth = len(dest_bb.getLoopHeaders())

            if dest_bb not in dests:
                f.write("0.0 ")
            elif len(dests) == 1:
                f.write("1.0 ")
            else:
                # Equal probability if both in the same loop
                if same:
                    f.write("0.5 ")
                # Skew probabilities to say in the loop, if not
                else:
                    # if dest_depth >= bb_depth:
                    if dest_bb.getLoopHeaders() == lh or dest_depth > bb_depth:
                        # f.write("{} ".format(1 - (0.10 / loop_exits[bb_loop])))
                        f.write("{} ".format(1 - (0.10)))
                    else:
                        # f.write("{} ".format((0.10 / 1)))
                        prob = 0.1
                        for i in range(bb_depth - dest_depth):
                            prob /= loop_exits[lh[i]]
                            print loop_exits[lh[i]]
                        print dest_depth,bb_depth, prob
                        f.write("{} ".format(prob))
        f.write("\n")
    f.write(";\n\n")

    f.close()

    # TODO proper temp file
    glpsol = pexpect.spawn("glpsol -d iterations.data -m {} -y /tmp/glp_iter".format(model), timeout=3600)
    glpsol.expect(".*OPTIMAL LP SOLUTION FOUND.*")
    glpsol.expect(pexpect.EOF)
    print "*** Found iteration count solution ***"
    loadIterations(file_cfgs, "/tmp/glp_iter")

    # edges = buildCallGraph(cfgs)
    # roots = findRootCFG(cfgs, edges)
    # # print "Found root:", cfg.findStartingBlocks(roots[0].basicblocks)[0].instructions[0].label

    # for r in roots:
    #     estimateIterations(r, cfgs, edges, estimate=0)



def createILPData(cfgs, fname, E_flash=100, E_ram=66, spare_ram=2000, max_cycle_factor=2, force_bbs=[], specified_only=False):
    f = open(fname, "w")

    all_bbs = list(itertools.chain(*map(lambda x: x.basicblocks, cfgs)))

    bb_names = []
    for bb in all_bbs:
        insn0 = bb.instructions[0]
        if insn0.label is False:
            bb_names.append("{}_{}".format(insn0.file,insn0.lineno))
        else:
            bb_names.append("{}_{}".format(insn0.file,insn0.label))

    bb_map = dict(zip(bb_names, all_bbs))

    f.write("set BBs := {};\n\n".format(" ".join(bb_names)))

    f.write("param usize :=\n")
    maxname = max(map(len, bb_names))

    sys.stdout.write("Calculating sizes")
    for bb_name, bb in zip(bb_names, all_bbs):
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, bb.codeSize()))
        sys.stdout.write(".")
        sys.stdout.flush()
    print ""
    f.write(";\n\n")

    f.write("param cyc_cost :=\n")
    sys.stdout.write("Calculating cycle costs")
    for bb_name, bb in zip(bb_names, all_bbs):
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, bb.cycleCount()))
        sys.stdout.write(".")
        sys.stdout.flush()
    print ""
    f.write(";\n\n")

    f.write("param iterations :=\n")
    for bb_name, bb in zip(bb_names, all_bbs):
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, bb.iterations))
    f.write(";\n\n")

    f.write("param force_ram :=\n")
    for bb_name, bb in zip(bb_names, all_bbs):
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, 1 if bb in force_bbs else 0))
    f.write(";\n\n")

    f.write("param force_flash :=\n")
    for bb_name, bb in zip(bb_names, all_bbs):
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, 1 if specified_only and bb not in force_bbs else 0))
    f.write(";\n\n")

    f.write("param icost_ram :=\n")
    for bb_name, bb in zip(bb_names, all_bbs):
        # Count number of calls in bb
        calls = sum(bb.countCalls().values())

        if bb.getTailInsn().operator in ["cbz", "cbnz"]:
            icost = 8
        elif not bb.getTailInsn().isBranch():
            icost = 6 # Fallthrough
        elif bb.getTailInsn().isUnconditional():
            icost = 2 # Unconditional branch
        else:
            icost = 6 # Conditional

        icost += calls*2
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, icost))
    f.write(";\n\n")

    f.write("param icost_cyc :=\n")
    for bb_name, bb in zip(bb_names, all_bbs):
        # Count number of calls in bb
        calls = sum(bb.countCalls().values())

        if bb.getTailInsn().operator in ["cbz", "cbnz"]:
            icost = 8 - 3
        elif not bb.getTailInsn().isBranch():
            icost = 4 # Fallthrough
        elif bb.getTailInsn().isUnconditional():
            icost = 4 - 3 # Unconditional branch
        else:
            icost = 7 - 3 # Conditional

        icost += calls*2
        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, icost))
    f.write(";\n\n")

    f.write("param icost_cyc_ram :=\n")
    for bb_name, bb in zip(bb_names, all_bbs):
        # Count number of calls in bb
        icost = 0

        for insn in bb.instructions:
            if insn.isLoad() or insn.isStore():
                icost += 2
#                icost += insn.cycleCount()
#            icost += 1


        f.write("\t{1: <{0}} {2}\n".format(maxname, bb_name, icost))
    f.write(";\n\n")


    f.write("param successors : {} :=\n".format(" ".join(bb_names)))
    for bb_name in bb_names:
        f.write("\t{1: <{0}}\t\t".format(maxname, bb_name))
        dests = bb_map[bb_name].destinations

        for bb_name2 in bb_names:
            f.write("{:d} ".format(bb_map[bb_name2] in dests))
        f.write("\n")
    f.write(";\n\n")

    f.write("param E_flash := {};\n".format(E_flash))
    f.write("param E_ram := {};\n".format(E_ram))
    f.write("param spare_ram := {};\n".format(spare_ram))
    f.write("param max_cycle_factor := {};\n".format(max_cycle_factor))

    f.write("end;\n")
    f.close()

    return dict(zip(bb_names, all_bbs))

def solveILP(bb_names, model):
    target_bbs = []

    print "Starting the ILP solver..."
    # TODO proper temp file
    glpsol = pexpect.spawn("glpsol -d ilp.data -m {} -y /tmp/glp.{}".format(model,os.getpid()), timeout=3600)
    glpsol.expect(".*INTEGER OPTIMAL SOLUTION FOUND.*")
    glpsol.expect(pexpect.EOF)
    print "*** Found solution ***"

    f = open("/tmp/glp.{}".format(os.getpid()))
    lines = f.readlines()
    cost = int(lines[1].split(":")[1])
    cycles = int(lines[3].split(":")[1])
    ramsize = int(lines[6].split(":")[1])
    totalsize = 0

    print "*** Cost:", cost
    # print cost.strip(),

    for l in lines:
        if l[0] == '#':
            print l.strip()
            continue

        parts = l.split(',')

        if parts[0] not in bb_names:
            print "ERROR", parts[0]
        else:
            if parts[2].strip() == "1":
                target_bbs.append(bb_names[parts[0]])
                totalsize += int(parts[1].strip())
            if parts[3].strip() == "1":
                bb_names[parts[0]].instrumented=1


    print "*** There are {} basicblocks in RAM".format(len(target_bbs))
    print "*** {} bytes of RAM used for code".format(totalsize)

    # print len(target_bbs), totalsize,

    return target_bbs, cost,cycles,ramsize

def preCompile(extra_flags="", doclean=True):
    global safe_register

    pexpect.run("make clean")

    out = pexpect.run("make CFLAGS=\"-ffixed-{} -g0 -save-temps -fstack-usage {}\"".format(safe_register, extra_flags), withexitstatus=True)

    if out[1] != 0:
        print out[0]
        raise RuntimeError("Make didn't succeed")

def doCompile(asmfiles, extra_flags=""):
    global safe_register

    pexpect.run("make clean")

    print "Applying changes"

    for f in asmfiles:
        print "    Assembling:",f
        parts = f.split(".")
        ofile = ".".join(parts[:-1]) + ".o"
        out = pexpect.run("arm-none-eabi-gcc -x assembler -c -g {}.out -o {}".format(f, ofile), withexitstatus=True)
        if out[1] != 0:

            if "Error: branch out of range" in out[0]:
                print "        Fixing out of range branches"
                fixed = False
                for i in range(10):
                    changes = []

                    flines = open(f+".out", "r").readlines()

                    for l in out[0].split('\n'):
                        m = re.match(r'.*:(\d+): Error: branch out of range', l)
                        if m is not None:
                            lineno = int(m.group(1))
                            print "\t\tBranch out of range, attempt to fix line", lineno
                            m2 = re.match(r'\s*(cbn?z)\s+([a-z0-9]+),\s*([A-Z.a-z0-9_]+)', flines[lineno - 1])
                            if m2 is not None:
                                print "\t\tFixable branch"
                                code = "    cmp {}, #0\n" \
                                       "    b{} {}".format(m2.group(2), "eq" if m2.group(1) == "cbz" else "ne", m2.group(3))
                                changes.append({"code_before": (lineno, code), "code_remove": (lineno-1,)})
                            else:
                                print "\t\tCant fix :("

                    out_lines = applyChanges(flines, changes)
                    print "\tApplying extras changes to", f
                    fp = open(f+".out."+str(i),"w")
                    fp.write("".join(out_lines))
                    fp.close()
                    out = pexpect.run("arm-none-eabi-gcc -x assembler -c -g {}.out.{} -o {}".format(f, i, ofile), withexitstatus=True)

                    if out[1] == 0:
                        fixed = True
                        break

                if fixed:
                    continue

            raise RuntimeError("Make didn't succeed")

    print "Linking..."
    pexpect.run("make CFLAGS=\"-ffixed-{} -save-temps -fstack-usage {}\"".format(safe_register, extra_flags))
    print "Done"


def main(compile=False, solve=False, maxram=1000, files=[], model="", cflags="", extrabbs=[], max_cycle_factor=1.5, specified_only=False, iteration_file=None, solveiters=False, itermodel="", iteration_estimate=10):
    file_cfgs = {}
    file_insns = {}
    file_lines = {}
    file_changes = {}
    file_fallthrough = {f:[] for f in files}
    call_sites = []

    if compile:
        preCompile(extra_flags=cflags)

    print "\n\n*** LOADING + CFG + CALL GRAPH *****************************"
    print "Loading instructions from assembly files"
    for f in files:
        insns, lines, cs = loadInstructions(f)
        call_sites += cs

        file_insns[f] = insns
        file_lines[f] = lines
        file_changes[f] = []
        print "\t", f

    print "Found {} call sites".format(len(call_sites))

    for f in files:
        cfgs = constructCFGs(file_insns[f], call_sites)
        file_cfgs[f] = cfgs

    cfg_list = reduce(list.__add__, file_cfgs.values(), [])

    edges = buildCallGraph(cfg_list)

    print "\n\n*** ITERATION ESTIMATION ***********************************"
    roots = findRootCFG(cfg_list, edges)
    print "Using root to estimate iterations:", cfg.findStartingBlocks(roots[0].basicblocks)[0].instructions[0].label

    for r in roots:
        estimateIterations(r, cfg_list, edges, estimate=iteration_estimate)

    if iteration_file is not None:
        loadIterations(file_cfgs, iteration_file)

    print "\n\n*** APPLYING BASIC BLOCK MODEL *****************************"
    if extrabbs:
        print "Forcing specified basic blocks into RAM"
    target_bbs = []
    # Add the basicblocks specified on the command line
    for n in extrabbs:
        f, l = n.split(':')
        for c in file_cfgs[f]:
            for bb in c.basicblocks:
                if bb.instructions[0].lineno == int(l):
                    if bb not in target_bbs:
                        target_bbs.append(bb)

    if solve:
        bb_names = createILPData(cfg_list, "ilp.data", spare_ram=maxram, max_cycle_factor=max_cycle_factor, force_bbs=target_bbs, specified_only=specified_only)
        target_bbs, cost, cycles, ramsize = solveILP(bb_names, model=model)
    else:
        print "Skipping the ILP solver"
        cost, cycles, ramsize = 0,0,0

    print "Basic blocks in RAM:", len(target_bbs)
    # for f in files:
    #     for c in file_cfgs[f]:
    #         for bb in c.basicblocks:
    #             if bb in target_bbs:
    #                 print "   ",f+":"+str(bb.instructions[0].lineno)

    print "\n\n*** DRAWING CFGS *******************************************"

    for f in files:
        print "CFGs in ",f
        for c in file_cfgs[f]:
            for bb in c.basicblocks:
                if bb in target_bbs:
                    bb.inram = True
                # print bb.instructions[0].lineno, map(lambda x: x.instructions[0].lineno, target_bbs)
        drawCFGs(file_cfgs[f], prefix=f)

    print "\n\n*** APPLYING TRANSFORMATIONS TO BASIC BLOCKS ***************"

    for fname, cfgs in file_cfgs.items():
        print "Transforming", fname
        for c in cfgs:
            for bb in c.basicblocks:

                cc = transformReferences(bb)
                file_changes[fname].extend(cc)

                ram_dests = filter(lambda x: x in target_bbs, bb.destinations)

                # If bb is not in ram, and some destinations are
                if bb not in target_bbs and len(ram_dests) > 0:
                    cc, fallthrough = instrumentBB(bb)
                    file_changes[fname].extend(cc)
                    file_fallthrough[fname].extend(fallthrough)

                # If bb is in ram and one of its destinations is not
                elif bb in target_bbs and len(ram_dests) != len(bb.destinations):
                    cc, fallthrough = instrumentBB(bb)
                    file_changes[fname].extend(cc)
                    file_fallthrough[fname].extend(fallthrough)

    for fname, cfgs in file_cfgs.items():
        for c in cfgs:
            for bb in c.basicblocks:

                if bb in target_bbs:
                    cc = markRAMBB(bb)
                    file_changes[fname].extend(cc)


    # for bb in target_bbs:
    #     cc = instrumentTargetBB(bb)
    #     file_changes[bb.instructions[0].file].extend(cc)

    # # TODO transform all
    # tables = []
    # for fname, cfgs in file_cfgs.items():
    #     print "Transforming jumptable:", fname
    #     bbs = reduce(list.__add__, map(lambda c: c.basicblocks, cfgs), [])
    #     tables.append(transformJumpTables(bbs, file_changes[fname], fname))

    # createGlobalTable(tables, file_changes[files[0]])

    for fname, cfgs in file_cfgs.items():
        for c in cfgs:
            for bb in c.basicblocks:
                file_changes[fname].extend(breakpointBB(bb))

    for fname in files:
        out_lines = applyChanges(file_lines[fname], file_changes[fname] + file_fallthrough[fname])

        print "Applying changes to", fname
        f = open(fname+".out","w")
        f.write("".join(out_lines))
        f.close()

    if compile:
        doCompile(files,extra_flags=cflags)

    return cost,cycles,ramsize

if __name__=="__main__":
    arguments = docopt(__doc__)

    model = "ilp.mod"
    itermodel = "iterations.mod"

    model = os.getcwd() + "/" + model
    itermodel = os.getcwd() + "/" + itermodel
    os.chdir(arguments['DIRECTORY'])

    print "Doing a make to work out what files are produced"

    preCompile(extra_flags=arguments['--flags'])
    asmfiles = glob.glob("*.s")

    print "Operating on files:"
    print "   ","\n    ".join(asmfiles)
    print "CFLAGS:",arguments['--flags']
    print "Max RAM:",arguments['--maxram']
    print "Max time:",arguments['--maxtime']
    print "Iteration file:",arguments['--iterations']


    if arguments['--maxram'] is None:
        arguments['--maxram'] = 1000

    main(solve=arguments['--solve'], compile=True,
        maxram=arguments['--maxram'], files=asmfiles,
        model=model, cflags=arguments['--flags'], extrabbs=arguments['--bb'],
        max_cycle_factor=float(arguments['--maxtime']),
        iteration_file=arguments['--iterations'],
        itermodel=itermodel,
        iteration_estimate=int(arguments['--estimate']))
